call  git fetch --all
call  git reset --hard origin/main
call git pull -unshallow
mshta "about:<script>alert('SRM actualizado existosamente');close()</script>"