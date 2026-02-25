# GUI implementation (MVP)

## Goal
For the existing market management system, a graphical interface was added while preserving a single business core and support for both launch modes:
- CLI
- GUI

## Selected pattern: MVP

### Model
- Domain dataclasses and aggregate state: `models.py`
- Business rules and use cases: `service.py`
- JSON persistence: `storage.py`

### Presenter
- `presenter.py`
- Accepts raw input from View (strings), validates/parses it, calls use-cases through application layer, and prepares tabular/report data for rendering.
- Does not contain any UI toolkit code.

### View
- `gui.py` (`Tkinter`/`ttk`)
- Contains only rendering and event binding.
- Delegates all operations to Presenter and refreshes tables/summary after each action.

## Shared code between CLI and GUI
A common application layer `application.py` was introduced:
- wraps `FairService` + `DataStore`
- centralizes all commands (`create_vendor`, `trade`, `report` data, etc.)
- persists data automatically after each mutating operation

Both clients now use the same backend flow:
- CLI: `cli.py -> FairApplication`
- GUI: `gui.py -> FairPresenter -> FairApplication`

This removes logic duplication and guarantees consistent behavior.

## Feature coverage in GUI
GUI includes all management capabilities available in CLI:
- market initialization
- venues/traders/buyers/stalls creation
- stall assignment
- products creation
- sell and advanced trade operations
- stock load/unload
- promotions and attractions
- vendor report
- full state visualization (tabs for vendors, buyers, venues, stalls, goods, sales, promotions, attractions, summary)

## Run modes

### CLI
```bash
python -m lab4 --data fair_data.json report
```

### GUI
```bash
python -m lab4 --gui --data fair_data.json
```

> `--gui` is handled in `__main__.py` and routes execution to the GUI entry point.
