describe 'something silly', ->

  it 'multiplies by 2', ->
    double = require 'hello'
    result = double 2
    expect(result).to.equal 4
