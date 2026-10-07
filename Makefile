.PHONY: test bench bench-eval eval demo demo-eval clean

PYTHON ?= python3

test:
	$(PYTHON) -m unittest discover -s tests -p "test_*.py" -v

bench:
	$(PYTHON) benchmarks/bench_skills.py

bench-eval:
	$(PYTHON) benchmarks/run_swe_hermes_eval.py

eval:
	$(PYTHON) -m unittest tests/test_eval_and_evolution.py -v

demo:
	$(PYTHON) examples/hermes_paperclip_demo.py

demo-eval:
	$(PYTHON) examples/hermes_swe_e2e_demo.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf build dist *.egg-info
