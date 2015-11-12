(defun run-python-tests (root-dir test-subdir buffer-name)
  (interactive)
  (if (projectile-project-p)
      (let ((default-directory (projectile-project-root))
            (buff (get-buffer-create buffer-name)))
        (display-buffer buff)
        (with-current-buffer buff
          (read-only-mode 0))
        (shell-command (concat "python -m unittest discover " test-subdir) buff)
        (with-current-buffer buff
          (compilation-mode)))))

;; This hook runs the tests after each save, a TDD-esque workflow.
(add-hook 'after-save-hook
          (lambda () (run-python-tests "c:/projects/bespoke"
                                       "test"
                                       "*python-tests*")))
