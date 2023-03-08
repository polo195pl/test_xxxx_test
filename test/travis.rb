#!/usr/bin/env ruby
result = `sass navoica_enroll/static/sass/project.scss navoica_enroll/static/css/project.css`
raise result unless $?.to_i == 0
raise "When compiled the module should output some CSS" unless File.exists?('built.css')
puts "Regular compile worked successfully"
