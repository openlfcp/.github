# OpenLFCP Project Narrative

## 1. Что мы строим

Мы строим **OpenLFCP**, открытый стек для local-first collaboration.

Исходная задача была очень конкретной: сделать совместные задачи в Obsidian, не превращая Obsidian в очередной облачный workspace и не отдавая личную базу заметок стороннему сервису.

Из этой задачи постепенно выросла более общая архитектура.

Основная идея OpenLFCP:

> Пользователь продолжает владеть своими локальными файлами и своим рабочим пространством. Совместными становятся только те объекты или документы, которые он явно решил разделить.

Совместный объект получает стабильную идентичность, локальную CRDT-реплику, правила доступа и маршруты синхронизации. Он может отображаться внутри разных локальных документов, у разных пользователей и даже в разных редакторах.

Серверы помогают репликам встретиться и обменяться изменениями, но не являются владельцами объекта.

---

# 2. Откуда появилась задача

Первоначальный use case появился из Obsidian.

Obsidian хорош именно тем, что Markdown-файлы находятся у пользователя. Их можно читать без Obsidian, хранить в Git, копировать, индексировать, обрабатывать скриптами и открывать через десять лет.

Но у этой модели есть слабое место: collaboration.

Например пользователь ведет Tasks:

```md
- [ ] Подготовить API contract
- [ ] Проверить pricing
- [ ] Позвонить клиенту
```

Он хочет разделить одну из этих задач с коллегой.

Обычные collaborative продукты предлагают примерно следующее решение:

```text
создать workspace
→ перенести туда данные
→ пригласить коллег
→ работать внутри сервиса
```

Но это меняет модель владения данными.

Мы хотим обратное.

Пользователь оставляет свой документ локальным:

```md
# Launch

Мои личные мысли про проект.

- [ ] Подготовить API contract

Еще несколько личных заметок.
```

И делает совместной только задачу:

```md
# Launch

Мои личные мысли про проект.

- [ ] Подготовить API contract <!-- lfcp-ref: ... -->

Еще несколько личных заметок.
```

Коллега вообще не обязан видеть `Launch.md`.

У него та же задача может находиться в совершенно другом файле:

```md
# This week

- [ ] Подготовить API contract <!-- lfcp-ref: ... -->
```

Это разные Markdown-файлы и один shared Task.

Если коллега завершает задачу:

```md
- [x] Подготовить API contract
```

у первого пользователя его локальная projection тоже становится:

```md
- [x] Подготовить API contract
```

При этом окружающие личные заметки никогда никуда не отправлялись.

Именно отсюда начинается вся архитектура OpenLFCP.

---

# 3. Главная продуктовая идея

OpenLFCP не должен заставлять пользователя переходить в shared workspace.

Наоборот:

> Shared world должен приходить отдельными объектами внутрь личного workspace пользователя.

То есть вместо:

```text
Organization
    └── Workspace
         └── Document
              └── Task
```

мы строим:

```text
My local workspace
    │
    ├── private document
    │     └── shared Task A
    │
    ├── private document
    │     ├── shared Task B
    │     └── shared Decision C
    │
    └── private document
```

Причем разные shared objects могут принадлежать разным группам людей.

Например одна локальная заметка пользователя может содержать:

```text
рабочую задачу
    → company collaboration

задачу с партнером
    → founders collaboration

семейную задачу
    → family collaboration
```

Эти collaboration contexts могут использовать разные LFCP Resources и даже разные серверы.

Для пользователя это по-прежнему один локальный Markdown-документ.

---

# 4. Почему мы не просто синхронизируем Markdown-файлы

Можно было бы взять Yjs или Automerge и сделать весь `.md` файл одним CRDT-документом.

Такой режим нам, вероятно, тоже понадобится.

Но это не лучший первый primitive.

Если sharing boundary проходит по документу, пользователь вынужден поделиться всем документом.

Кроме того, целые Markdown-файлы создают множество специфических конфликтов: перемещение секций, formatter-ы, Obsidian plugins, изменение frontmatter, внешнее редактирование файла, Git checkout и так далее.

Shared objects дают более интересную модель.

Например:

```text
Task
Decision
Approval
Comment thread
Project status
```

каждый может иметь собственную collaborative identity, но отображаться внутри обычного Markdown.

Поэтому первая реализация OpenLFCP для Obsidian строится вокруг **Shared Objects**, а whole-document collaboration рассматривается как следующий отдельный режим.

---

# 5. Resource и Object

В архитектуре есть два разных уровня.

**LFCP Resource** является security и collaboration boundary.

Он определяет участников, encryption keys, routing, ownership и Control Plane.

Один Resource обычно содержит много объектов:

```text
Resource: Project Alpha

    task A
    task B
    task C
    decision D
    approval E
```

Мы специально не делаем каждый Task отдельным LFCP Resource. Это создало бы огромный overhead на ACL, routing, encryption epochs и control records.

**Shared Object** является прикладной сущностью внутри Resource.

Полная идентичность объекта выглядит концептуально как:

```text
LFCP Resource ID
+
Object type
+
Object ID
```

Например:

```text
lfcp1:RESOURCE#task:OBJECT
```

Эта ссылка остается стабильной независимо от того:

- в каком Markdown-файле находится projection;
- как называется файл;
- где находится vault;
- какой редактор используется;
- на каком сервере сейчас синхронизируется Resource;
- кто является текущим owner.

---

# 6. Один объект может иметь много projections

Это важное свойство системы.

Один shared Task может одновременно находиться у одного пользователя в:

```text
Today.md
Project Alpha.md
Important.md
Pavel.md
```

и у другого пользователя в:

```text
Work.md
This Week.md
```

Это не шесть Tasks.

Это шесть projections одного объекта.

Изменение любой projection изменяет shared object, после чего остальные projections обновляются.

Поэтому Markdown является не единственным source of truth, а **локальной редактируемой проекцией collaborative state**.

При этом пользователь не должен ощущать себя внутри абстрактного CRDT UI. Он продолжает работать с обычным Markdown.

---

# 7. Что такое LFCP

Когда мы начали разбирать инфраструктуру для этих объектов, стало понятно, что сама проблема гораздо шире Obsidian.

Нам нужен протокол, который позволяет нескольким локальным приложениям реплицировать collaborative Resources через заменяемые серверы.

Так появился **LFCP, Local-First Collaboration Protocol**.

Obsidian не является частью LFCP Core.

VS Code тоже не является частью LFCP Core.

LFCP отвечает за:

```text
identity
authorization
encryption
resource identity
control state
routing
replication
transport
```

Application Profile отвечает за структуру collaborative data.

Editor adapter отвечает за пользовательский интерфейс.

Таким образом:

```text
Obsidian
     │
Shared Objects Profile
     │
LFCP Client
     │
LFCP Protocol
     │
LFCP Server(s)
```

---

# 8. Сервер не является владельцем данных

Это фундаментальная архитектурная установка.

В обычном SaaS:

```text
server
  owns canonical database
```

В OpenLFCP:

```text
clients own replicas

server = rendezvous + durable replication peer
```

LFCP server может:

- хранить encrypted Data Units;
- хранить snapshots;
- хранить Control Records;
- передавать updates;
- обеспечивать presence;
- координировать security-sensitive Control Plane transitions;
- применять quota и hosting policy.

Но сервер не должен владеть семантической истиной Resource.

У пользователя могут быть:

```text
Resource A → Server A
Resource B → Server B
Resource C → Server C
```

Один Resource в будущем может иметь несколько sync endpoints.

При смене сервера Resource ID не меняется.

---

# 9. Федеративная модель

Пользователь не принадлежит одному LFCP server.

Это принципиально.

Не существует обязательного:

```text
my server = server X
```

Вместо этого есть:

```text
Resource A can be found through endpoint X
Resource B can be found through endpoint Y
```

Например:

```text
Andrey

Project Alpha
    → sync.company.example

Founders
    → sync.pavel.example

Family
    → home-server.example
```

Другой участник тех же Resources может иметь совершенно другой набор collaboration contexts.

Таким образом постепенно возникает federated network.

Серверы могут быть:

- личными;
- командными;
- корпоративными;
- публичными hosted services;
- временными;
- зеркалами друг друга.

Протокол не требует одного глобального сервера.

---

# 10. Identity, Authorization, Encryption и Routing являются разными вещами

Одной из самых важных архитектурных ошибок было бы смешать их.

OpenLFCP сознательно разделяет четыре вопроса.

**Identity:** кто выполняет действие?

**Authorization:** что этой identity разрешено?

**Encryption:** кто способен прочитать содержимое?

**Routing:** через какие peers или серверы можно получить данные?

Например пользователь может сохранить одну identity, перенести Resource на новый сервер и не менять ни ACL, ни Resource ID.

Или сервер может знать, что некоторому account разрешено потреблять storage quota, но это не делает этот account владельцем Resource.

---

# 11. Централизованный аккаунт не является root of trust

Для LFCP protocol наличие глобального аккаунта вообще не обязательно.

Протокол может работать через:

```text
cryptographic Principal
+
invitation
+
resource key
+
routes
```

Hosted service позже может предоставить:

```text
email login
OAuth
passkeys
contact discovery
push notifications
billing
key backup
```

Но это usability layer.

Удаление OpenLFCP hosted service не должно уничтожать identity Resources или ownership пользователей.

---

# 12. Data Plane и Control Plane

LFCP разделяет два типа состояния.

**Data Plane** содержит пользовательские collaborative изменения.

Например:

```text
Task status changed
Task title changed
tag added
text edited
comment added
```

Data Plane является multi-writer и рассчитан на concurrent offline updates.

Здесь используется CRDT.

**Control Plane** содержит security-sensitive state:

```text
ownership
capabilities
revocations
key epochs
routing
invite claims
```

Такие операции нельзя просто merge-ить как обычный Task title.

Поэтому LFCP-WIRE-01 использует сериализованный per-resource Control Chain и заменяемый **Control Coordinator**.

Coordinator не становится владельцем данных. Он только обеспечивает deterministic ordering security-sensitive transitions.

---

# 13. Encryption

Shared Resource имеет симметричный Data Encryption Key для текущего encryption epoch.

LFCP servers в нормальном режиме получают encrypted payload.

При добавлении участников им передаются Resource keys через encrypted Key Packages.

При security-sensitive удалении участника создается новый epoch и новый key.

Важно понимать ограничение:

> Нельзя заставить пользователя забыть данные, которые он уже когда-то расшифровал.

Revocation защищает будущие изменения, а не стирает прошлое из памяти бывшего участника.

---

# 14. CRDT engine не является LFCP

LFCP специально не привязан к одному CRDT implementation.

Resource Genesis содержит Data Profile.

Например будущие профили могут использовать:

```text
Automerge
Yjs
другой CRDT
```

Для первого Shared Objects Profile мы выбрали **Automerge**.

Причина проста: наша начальная задача является скорее collaborative structured state problem, чем simultaneous text-editing problem.

Shared Task естественно выглядит как структура:

```text
title
status
due
priority
tags
assignees
```

Automerge хорошо подходит для такого состояния, сохраняет concurrent scalar conflicts и позволяет local-first replicas.

Серверу знать про Automerge не нужно.

Для него CRDT payload остается encrypted opaque bytes.

---

# 15. Shared Objects Profile

Первый application profile называется:

```text
org.openlfcp.shared-objects.v1
```

Один Resource содержит Automerge document:

```text
objects
    ├── object A
    ├── object B
    └── object C
```

Первая стандартизированная сущность:

```text
Task
```

Позже могут появиться:

```text
Decision
Approval
Comment Thread
Project Status
```

Но Task является первым reference object, потому что он позволяет проверить практически все необходимые свойства системы.

---

# 16. Конфликты являются частью продукта

CRDT не означает отсутствие конфликтов.

CRDT означает, что replicas способны технически сойтись без потери concurrent operations.

Например:

```text
Andrey offline:
status = done

Pavel offline:
status = cancelled
```

После synchronization мы не хотим случайно выбрать последнее изменение.

Shared Objects Profile сохраняет semantic conflict:

```text
status:
    done
    cancelled
```

UI может временно показать одно из значений, но обязан сообщить, что поле конфликтно.

Пользователь выбирает:

```text
done
```

и новая causal write разрешает конфликт.

То же относится к title, lifecycle и некоторым другим scalar fields.

---

# 17. Collections имеют свои merge rules

Не все поля должны создавать UI conflicts.

Например Tags и Assignees в первой версии реализуются как add-wins sets.

Если один offline peer удаляет:

```text
backend
```

а второй одновременно добавляет тот же tag, после convergence tag остается.

Это application semantics, а не LFCP semantics.

LFCP знает только encrypted Data Unit.

Shared Objects Profile знает, что это означает.

---

# 18. Удаление является tombstone

Shared Object обычно не удаляется физически из CRDT.

Удаление означает:

```text
lifecycle = deleted
```

Причина очень практическая.

Представим:

```text
Peer A:
delete Task

Peer B offline:
rename Task
```

Если физически удалить map object, concurrent работа второго пользователя может просто исчезнуть.

При tombstone получается:

```text
lifecycle = deleted
title = new title
```

Task считается удаленным, но concurrent edit сохраняется.

Если Task позже восстановить, данные все еще существуют.

---

# 19. Obsidian является первым reference client

Первый реальный пользовательский продукт поверх OpenLFCP мы строим для Obsidian.

Но Obsidian plugin не должен становиться владельцем протокола.

Dependency direction:

```text
LFCP specs
    ↓
TypeScript SDK
    ↓
Shared Objects Profile implementation
    ↓
Obsidian adapter
```

Obsidian отвечает за:

```text
Markdown scanning
Task parsing
Markdown refs
projection updates
CodeMirror decorations
Resource Explorer
invite UI
conflict UI
settings
```

Он не должен самостоятельно реализовывать cryptography или LFCP Wire.

---

# 20. Obsidian Task flow

Локально пользователь пишет:

```md
- [ ] Prepare API contract
```

Вызывает:

```text
LFCP: Share task under cursor
```

Выбирает collaboration Resource:

```text
Project Alpha
```

Plugin:

```text
parses Markdown task
→ creates Shared Object
→ creates Automerge change
→ creates LFCP Data Unit
→ adds LFCP ref into Markdown
```

Получается:

```md
- [ ] Prepare API contract <!-- lfcp-ref: lfcp1:RESOURCE#task:OBJECT -->
```

или, в равнозначной child-line форме:

```md
- [ ] Prepare API contract
  <!-- lfcp-ref: lfcp1:RESOURCE#task:OBJECT -->
```

Обе формы (inline и immediate child-line) conforming по `MARKDOWN-REFS-01`; для Obsidian по умолчанию рекомендуется child-line.

Remote peer может вставить тот же shared Task в свой локальный документ.

Теперь изменения распространяются через LFCP.

---

# 21. Markdown должен оставаться нормальным Markdown

OpenLFCP не должен превращать Markdown-файлы в непрочитаемый служебный формат.

Даже без plugin пользователь должен видеть:

```md
- [ ] Prepare API contract
```

а не огромный сериализованный CRDT block.

LFCP metadata должна быть минимальной и portable.

На текущем архитектурном уровне предпочтительный вариант:

```md
<!-- lfcp-ref: ... -->
```

Точная грамматика зафиксирована в `MARKDOWN-REFS-01`: comment допустим как inline в конце Task line, так и на immediate child-line; обе формы семантически эквивалентны.

---

# 22. Совместимость с Obsidian Tasks

Мы не хотим писать собственную замену Tasks plugin.

OpenLFCP должен работать рядом с ним.

Tasks видит:

```md
- [ ] API contract 📅 2026-10-10
```

OpenLFCP видит:

```text
Task syntax
+
lfcp-ref
```

Поэтому привычные Obsidian workflows продолжают работать.

Это важная продуктовая установка:

> LFCP должен добавлять collaboration в существующий local workflow, а не заставлять пользователя перейти в новый task manager.

---

# 23. VS Code и другие редакторы

После Obsidian должен появиться VS Code extension.

Он будет использовать тот же:

```text
LFCP SDK
Shared Objects Profile
Markdown reference format
```

Но иметь свой UI.

Это позволит одному shared Task одновременно существовать в:

```text
Obsidian
VS Code
будущем Neovim plugin
browser todo app
standalone client
```

Таким образом Shared Object принадлежит протоколу, а не конкретному editor vendor.

---

# 24. Standalone examples важны не меньше plugin

Чтобы LFCP не выглядел как obscure Obsidian-specific technology, нужны очень простые reference applications.

Например:

```text
shared counter
todo web app
todo CLI
offline conflict demo
multi-server migration demo
```

`todo-web` должен позволять понять всю модель за пять минут:

```text
Browser A
Browser B
LFCP Server
```

Оба браузера редактируют shared tasks.

Один отключается.

Оба работают.

После reconnect replicas сходятся.

Это будет Hello World для LFCP.

---

# 25. Open-source структура проекта

Рабочее название GitHub organization:

```text
github.com/openlfcp
```

Сам протокол называется:

```text
LFCP
```

Проект и community:

```text
OpenLFCP
```

Основные repositories должны быть разделены по ответственности.

`openlfcp/spec` содержит только normative specification, profiles и test vectors.

`openlfcp/sdk-ts` содержит reusable TypeScript implementation.

`openlfcp/sdk-rs` дает независимую Rust implementation и проверяет, что LFCP действительно является protocol, а не TypeScript library convention.

`openlfcp/server` содержит open-source reference server.

`openlfcp/obsidian` содержит Obsidian adapter.

`openlfcp/vscode` позже содержит VS Code adapter.

`openlfcp/examples` содержит минимальные standalone applications.

Позже появятся `interop`, `cli`, `inspector` и website.

---

# 26. Reference server

Первая версия server должна быть намеренно маленькой.

Цель:

```text
one executable
```

или:

```text
one Docker container
```

Без обязательных:

```text
PostgreSQL
Redis
Kafka
S3
```

Для первого варианта достаточно SQLite и filesystem storage.

Server должен реализовывать:

```text
LFCP WebSocket transport
session authentication
Resource hosting
Control Coordinator
Control Record storage
encrypted Data Unit storage
snapshots
Key Packages
invite claims
presence
minimal admin API
```

Он не должен знать:

```text
Markdown
Tasks
Obsidian
Automerge semantics
```

---

# 27. Минимальный server UI

Self-hosted LFCP server не нуждается в полноценной системе регистрации.

При первом запуске он создаёт одноразовый pairing code и записывает его в файл `<state_dir>/setup-code` с правами 0600.

В stdout и в лог код не попадает: container runtimes их сохраняют (`docker logs`). В лог пишется только путь:

```text
pairing code written to /var/lib/lfcp/setup-code (expires in 60 minutes; pair an LFCP Principal at /setup/pair)
```

Оператор читает код из этого файла и открывает `/setup`. После pairing файл удаляется.

Пользователь открывает web page и связывает свой LFCP Principal с server administrator role.

Это server-level administration.

Не Resource ownership.

Hosted public server позже может добавить email/OAuth/passkeys для quota, billing и usability.

Но эти accounts не должны становиться root of trust LFCP Resources.

---

# 28. Что уже спроектировано

На данный момент архитектурная работа уже прошла несколько уровней.

Существует общий LFCP protocol narrative.

Существует `LFCP-WIRE-01`, определяющий wire protocol.

Бывшие errata `LFCP-WIRE-01.1`, исправлявшие byte-level неоднозначности, уже встроены в `LFCP-WIRE-01`; отдельного активного документа `LFCP-WIRE-01.1` нет.

Существует `LFCP-TEST-VECTORS-01`.

Существует `OBSIDIAN-ARCHITECTURE-01`.

Существует `SHARED-OBJECTS-PROFILE-01`.

Существует `SHARED-OBJECTS-TEST-VECTORS-01`.

Поэтому новые implementation agents не должны заново изобретать protocol architecture на каждом шаге.

Если implementation обнаруживает реальную неоднозначность или противоречие, это должно становиться issue/spec errata, а не локальной undocumented convention.

---

# 29. Роль test vectors

Test vectors являются ключевой частью проекта.

Мы хотим иметь независимые:

```text
TypeScript implementation
Rust implementation
```

которые проходят одни и те же vectors.

Там, где specification требует exact bytes, реализации должны получать byte-for-byte одинаковый результат.

Там, где Automerge допускает разные корректные бинарные representation, interoperability определяется иначе:

```text
implementation A produces change
implementation B can apply it

implementation B produces change
implementation A can apply it

same set of changes
    ↓
same logical state
    ↓
same conflict semantics
```

Цель не сделать две библиотеки одинаковыми внутри.

Цель доказать interoperability.

---

# 30. Высокоуровневая архитектура

Вся система выглядит так:

```text
                     OpenLFCP Specification

                  protocol / wire / profiles
                            │
             ┌──────────────┴──────────────┐
             ▼                             ▼

        TypeScript SDK                 Rust SDK
             │                             │
             │                             ▼
             │                       LFCP Server
             │
      ┌──────┼────────┐
      ▼      ▼        ▼

 Obsidian  VS Code   Web/CLI examples

      │
      ▼

Shared Objects Profile
      │
      ▼
Local CRDT replicas
      │
      ▼
LFCP encrypted Data Plane
      │
      ├──────────────┐
      ▼              ▼
 Server A          Server B
```

---

# 31. Что должно оставаться reusable

При реализации необходимо жестко следить за dependency boundaries.

Не должно происходить такого:

```text
LFCP SDK imports Obsidian
```

или:

```text
Server imports Automerge task semantics
```

Правильное направление:

```text
spec
 ↓
core implementations
 ↓
application profiles
 ↓
editor/application adapters
```

Shared Objects Profile тоже не принадлежит Obsidian.

Standalone Todo App должен использовать тот же профиль.

---

# 32. План реализации

Первый этап заключается не в красивом UI, а в interoperability foundation.

TypeScript SDK должен научиться читать и создавать объекты LFCP в соответствии с test vectors.

Rust implementation должна независимо подтвердить wire compatibility.

Reference server должен синхронизировать opaque encrypted resources между двумя клиентами.

После этого реализуется Shared Objects Profile в TypeScript.

Сначала полностью локально, без network dependency:

```text
create Task
edit Task
merge concurrent Task state
surface conflicts
tombstone
sets
snapshot
```

Следующий этап добавляет Markdown projection engine.

Нужно добиться такого:

```text
Markdown edit
→ semantic Task intent
→ CRDT state

CRDT state change
→ minimal Markdown update
```

После этого подключается реальный LFCP sync между двумя Obsidian vault.

Только когда этот end-to-end сценарий стабилен, имеет смысл серьезно полировать Resource Explorer, invitations и settings.

---

# 33. Первый обязательный end-to-end demo

Минимальный успех проекта должен выглядеть очень просто.

Есть:

```text
Vault A
Vault B
LFCP Server
```

Andrey создает:

```md
- [ ] Prepare API contract
```

делает Task shared.

Pavel получает invite.

У себя вставляет тот же Task в другой Markdown-файл.

Pavel завершает его.

У Andrey локальный Markdown автоматически становится:

```md
- [x] Prepare API contract
```

Затем Pavel отключается от сети.

Andrey и Pavel делают concurrent changes.

После reconnect state сходится.

Если изменения семантически совместимы, происходит автоматический merge.

Если они конфликтуют, появляется conflict UI.

После explicit resolution оба клиента снова видят одно состояние.

При этом ни один private Markdown paragraph не был отправлен на server.

Это первый критерий того, что идея работает.

---

# 34. Следующий demo должен показать federation

После базового сценария нужно показать два сервера.

Например:

```text
Resource A
→ Server A

Resource B
→ Server B
```

Оба shared Tasks находятся внутри одного Markdown-документа.

Один server отключается.

Task другого Resource продолжает работать.

Позже Resource A мигрирует на Server C без изменения object reference в Markdown.

Это будет демонстрацией того, что LFCP Resource действительно независим от server location.

---

# 35. Чего сейчас не надо делать

Не нужно преждевременно строить большую cloud platform.

Не нужно делать billing.

Не нужно делать глобальную социальную сеть identities.

Не нужно делать enterprise admin panel.

Не нужно делать весь Obsidian collaborative.

Не нужно поддерживать двадцать object types.

Не нужно оптимизировать server на миллион одновременных connections.

Не нужно добавлять Kafka потому, что «потом понадобится».

Первый вопрос гораздо проще:

> Работает ли модель shared collaborative objects внутри личных local-first documents настолько естественно, что люди захотят ею пользоваться?

Архитектура должна позволять большой системе появиться позже, но MVP должен оставаться маленьким.

---

# 36. Основные архитектурные инварианты

При принятии implementation decisions агенты должны сохранять следующие свойства.

Local Markdown принадлежит пользователю и не загружается целиком только потому, что содержит shared object.

LFCP Resource identity не зависит от сервера.

Shared Object identity не зависит от Markdown-файла.

Один Shared Object может иметь несколько projections.

Один Markdown-документ может содержать объекты из нескольких Resources.

Разные Resources могут использовать разные servers.

LFCP server не должен понимать application semantics.

Shared Objects Profile не должен зависеть от Obsidian.

Obsidian plugin не должен самостоятельно определять LFCP protocol semantics.

Offline operation является нормальным состоянием, а не исключением.

CRDT convergence не должно скрывать semantic conflicts.

Security-sensitive Control Plane state нельзя merge-ить как обычные application data.

Global account не является обязательным условием владения Resource.

Server migration не должна менять Resource или Object identity.

Unknown future profile data нужно сохранять, а не уничтожать.

---

# 37. Как оркестратор должен декомпозировать работу

Оркестратор должен мыслить слоями, а не UI-фичами.

Если задача относится к serialization, cryptography, Control Plane или wire messages, она относится к LFCP core/spec implementation.

Если задача относится к CRDT Task state, intents, conflict semantics или Shared Object validation, она относится к Shared Objects Profile.

Если задача касается Markdown parsing, CodeMirror decorations, commands или Obsidian settings, она относится к Obsidian adapter.

Если проблема обнаруживает неоднозначность normative behavior, агент не должен придумывать private fix только для своей реализации. Нужно определить, является ли это ошибкой implementation или дыркой specification.

Если это specification gap, результатом должен стать proposal/errata плюс тест.

---

# 38. Как coding agents должны работать со спецификациями

Агент должен сначала определить, какой документ является source of truth для его задачи.

Например:

```text
LFCP-WIRE
→ network / crypto / control / storage protocol

SHARED-OBJECTS-PROFILE
→ Task CRDT semantics

OBSIDIAN-ARCHITECTURE
→ editor integration
```

Если prose и test vectors расходятся, это нужно явно поднять как проблему.

Нельзя молча менять код так, чтобы он «проходил конкретный тест», если это противоречит normative specification.

И наоборот, если byte-level vector фиксирует нормативный deterministic encoding, нельзя заменить его «почти эквивалентным».

---

# 39. Как оценивать техническое решение

При наличии нескольких вариантов предпочтение следует отдавать варианту, который:

сохраняет local-first свойства;

уменьшает центральные точки доверия;

не усложняет MVP без необходимости;

оставляет protocol implementation независимой от конкретного editor;

оставляет server application-agnostic;

хорошо тестируется через независимые implementations;

позволяет пользователю экспортировать, перемещать и продолжать использовать данные без конкретного vendor.

OpenLFCP не должен становиться distributed системой ради distributed системы.

Federation, CRDT и cryptographic ownership нужны только там, где они защищают реальные свойства продукта.

---

# 40. Что в проекте является главным экспериментом

Наша гипотеза глубже, чем «людям нужны collaborative Tasks в Obsidian».

Гипотеза такова:

> Collaboration не обязана происходить внутри общего workspace. Люди могут оставаться в собственных локальных рабочих пространствах и разделять только отдельные объекты, которые появляются в каждом workspace в удобном для этого пользователя месте.

Если эта модель окажется удобной, она применима далеко за пределами Obsidian.

Например один Decision может отображаться:

```text
у одного человека в Markdown
у другого в VS Code
у третьего в standalone project client
```

При этом все работают с одним collaborative object.

Это превращает local-first workspace пользователя в персональную projection распределенного shared world.

---

# 41. Долгосрочное направление

Если базовая модель окажется успешной, OpenLFCP постепенно может расширяться.

Shared Objects смогут включать больше типов.

Появится whole-document collaborative mode.

Появятся attachments.

Resource сможет иметь несколько active replicas на разных servers.

Появятся direct peer transports.

Появятся richer identity discovery и recovery mechanisms.

Могут появиться commercial hosted LFCP services.

Но все эти уровни должны сохранять базовый принцип:

> Данные и collaborative identity объекта не должны становиться заложниками одного приложения или одного сервера.

---

# 42. Короткая формулировка проекта

Для человека:

> **OpenLFCP — открытый local-first протокол и набор инструментов, позволяющий добавлять совместные объекты и документы в локальные приложения без передачи владения данными центральному workspace.**

Для разработчика:

> **LFCP предоставляет portable Resource identity, cryptographic authorization, encrypted replication и replaceable sync servers. Application profiles определяют CRDT semantics, а editor adapters отображают эти Resources внутри локальных рабочих процессов.**

Для первого продукта:

> **Мы начинаем с shared Tasks внутри Obsidian: пользователь может встроить совместную задачу в личную Markdown-заметку, не делясь самой заметкой.**

---

# 43. North Star

Если архитектура развивается правильно, пользователь должен иметь возможность сделать следующее.

Сегодня он использует:

```text
Obsidian
+
personal LFCP server
```

Завтра он открывает те же collaborative Resources через:

```text
VS Code
```

Позже переносит server:

```text
server A
→
server B
```

Его Resource IDs не меняются.

Его shared Tasks не меняют identity.

Его collaborators не обязаны мигрировать в новый workspace.

Его private notes остаются его private notes.

Меняются приложения и инфраструктура.

**Collaborative data relationship остается.**

Это и есть OpenLFCP.