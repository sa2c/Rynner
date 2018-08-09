(setq python-current-test "running_integration")
(spacemacs/set-leader-keys "d" '(lambda ()
                                  (interactive)
                                  (let ((my-test-command (concat "pipenv run python -m tests."
                                                                 python-current-test)))
                                    (projectile-save-project-buffers)
                                    (projectile-with-default-dir (projectile-project-root)
                                      (async-shell-command my-test-command "*testing*")))))


;; Set python env manually
(progn
  (setq rynner-python-venv "/Users/markdawson/.local/share/virtualenvs/rynner-BD0iQRUE")
  (setq runner-pipenv-path "/usr/local/Cellar/pipenv/11.9.0/libexec/")
  (setenv "PYTHONDONTWRITEBYTECODE" "1")
  (setenv "PIP_PYTHON_PATH" (concat runner-pipenv-path "bin/python3.6"))
  (setenv "PYTHONUNBUFFERED" "1")
  (setenv "__CF_USER_TEXT_ENCODING" "0x1F8:0x0:0x2")
  (setenv "VIRTUAL_ENV" rynner-python-venv)
  (setenv "PIPENV_ACTIVE" "1")
  (setenv "PATH"
          (concat
           rynner-python-venv
           "/bin:"
           runner-pipenv-path
           "tools:"
           (getenv "PATH"))))
