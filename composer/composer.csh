# Composer initialization script

# Add path to commands installed using "composer global require ..."
if ( ${euid} > 0 ) then
  if ( "${path}" !~  *${HOME}/.composer/vendor/bin* ) then
   set path = ( $path ${HOME}/.composer/vendor/bin )
  endif
endif

