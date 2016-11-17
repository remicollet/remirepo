# Composer initialization script

# Add path to commands installed using "composer global require ..."
if [ "${EUID:-0}" != "0" ]; then
  case :$PATH: in
    *:${HOME}/.composer/vendor/bin:*) ;;
    *) PATH=$PATH:${HOME}/.composer/vendor/bin ;;
  esac
  export PATH
fi

