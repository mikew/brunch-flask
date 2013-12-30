def python_unittest(test_file)
  return unless File.exist? test_file

  system *[ 'server/tests/runner.py', test_file ]
end

guard 'shell' do
  watch %r{server/([^/]+/)*(.*).py$} do |m|
    # Since the tests/ directory lives inside server/ we use this check
    # to avoid doubling up.
    unless m[1].to_s.start_with? 'tests/'
      python_unittest "server/tests/#{m[1]}test_#{m[2]}.py"
    end
  end

  watch %r{server/tests/([^/]+/)*test_(.*).py$} do |m|
    python_unittest m[0]
  end

  watch %r{server/tests/__all__.py$} do |m|
    python_unittest 'server/tests/'
  end

end
