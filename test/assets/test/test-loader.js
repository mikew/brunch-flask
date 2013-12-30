window.require.list()
  .filter(function(name) {return /-test$.test(name)/;})
  .forEach(require);
