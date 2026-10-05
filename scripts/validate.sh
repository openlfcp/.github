#!/usr/bin/env bash
# Validation entry point for the organization .github repository.
#
# 1. every YAML file (workflows, issue forms, labels) is well-formed;
# 2. .github/labels.yml entries have a unique name, a 6-digit hex color and
#    a description;
# 3. every issue form has a name, a description and a non-empty body.
set -euo pipefail

cd "$(dirname "$0")/.."

ruby -ryaml - <<'RUBY'
files = Dir[".github/**/*.{yml,yaml}"].sort
files.each { |f| YAML.safe_load(File.read(f), aliases: true) }
puts ".github: #{files.size} YAML file(s) parsed"

problems = []
labels_file = ".github/labels.yml"
if File.exist?(labels_file)
  labels = YAML.safe_load(File.read(labels_file))
  problems << "#{labels_file}: must be a list" unless labels.is_a?(Array)
  names = []
  Array(labels).each_with_index do |l, i|
    where = "#{labels_file}[#{i}]"
    unless l.is_a?(Hash) && l["name"].is_a?(String) && !l["name"].empty?
      problems << "#{where}: missing name"
      next
    end
    problems << "#{where}: duplicate name #{l['name']}" if names.include?(l["name"])
    names << l["name"]
    problems << "#{where}: color must be 6 hex digits" unless l["color"].to_s.match?(/\A\h{6}\z/)
    problems << "#{where}: missing description" if l["description"].to_s.strip.empty?
  end
  puts ".github: #{names.size} label(s) checked"
end

forms = Dir[".github/ISSUE_TEMPLATE/*.{yml,yaml}"].reject { |f| File.basename(f, ".*") == "config" }.sort
forms.each do |f|
  form = YAML.safe_load(File.read(f))
  %w[name description].each { |k| problems << "#{f}: missing #{k}" if form[k].to_s.strip.empty? }
  problems << "#{f}: body must be a non-empty list" unless form["body"].is_a?(Array) && !form["body"].empty?
end
puts ".github: #{forms.size} issue form(s) checked" unless forms.empty?

problems.each { |p| puts "FAIL  #{p}" }
exit(problems.empty? ? 0 : 1)
RUBY
