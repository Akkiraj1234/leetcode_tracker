from LeetSolver.frontend import ui
from LeetSolver.backend import logic
from LeetSolver import initapp

def main():
    ui_id, settings = initapp(__path__)
    ui = ui(ui_id, settings.app)
    backend = logic(settings.backend, settings.database)
    backend.start(ui)
    
if __name__ == "__main__":
    main()
    