(require 'cl) 

(progn
  (setenv "RYNNER_TEST_HOST" "hawklogin.cf.ac.uk")
  (setenv "RYNNER_TEST_USER" "s.mark.dawson")
  (setenv "RYNNER_REMOTE_HOME" "/home/s.mark.dawson"))

(defun rynner-get-all-test-files ()
  (remove-if-not '(lambda (file)
                    (and (string-match ".py" file)
                         (not (string-match "__init__.py" file))))
                 (directory-files
                  (concat
                   (projectile-project-root)
                   "/tests/"))))

(setq python-current-test "test_running_integration")

(spacemacs/set-leader-keys "D" '(lambda ()
                                  (interactive)
                                  (let ((my-test-command (concat "pipenv run python -m tests."
                                                                 python-current-test)))
                                    (projectile-save-project-buffers)
                                    (projectile-with-default-dir (projectile-project-root)
                                      (async-shell-command my-test-command "*testing*"))
                                    (with-current-buffer "*testing*"
                                        (evil-normal-state)))))

(setq my-tests-to-run "test_plugin_integration")

(spacemacs/set-leader-keys "D" '(lambda ()
                                  (interactive)
                                  (setq my-tests-to-run (read-string "test module: " ))))

(spacemacs/set-leader-keys "d" '(lambda ()
                                  (interactive)
                                  (let ((my-test-command
                                         (concat "pipenv run -- python -m unittest tests." my-tests-to-run)))
                                    (projectile-save-project-buffers)
                                    (projectile-with-default-dir (projectile-project-root)
                                      (async-shell-command my-test-command "*testing*"))
                                    (with-current-buffer "*testing*"
                                      (compilation-shell-minor-mode)
                                      (evil-normal-state)
                                      ))))

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
