(defun run-python-tests (root-dir test-subdir buffer-name)
  (interactive)
  (let ((default-directory (file-name-as-directory root-dir))
        (buff (get-buffer-create buffer-name)))
    (if (projectile-project-p)
        (progn (display-buffer buff)
               (with-current-buffer buff
                 (read-only-mode 0))
               (shell-command (concat "c:/python34/python -m unittest discover " test-subdir) buff)
               (with-current-buffer buff
                 (compilation-mode))))))

(defun run-bespoke-tests ()
  (run-python-tests "c:/projects/bespoke"
                    "test"
                    "*python-tests*"))

;; This hook runs the tests after each save, a TDD-esque workflow.
(add-hook 'after-save-hook
          'run-bespoke-tests)
