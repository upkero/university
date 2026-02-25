from __future__ import annotations

import argparse
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk
from typing import Callable

from .errors import FairError
from .presenter import FairPresenter

DEFAULT_DATA_FILE = "fair_data.json"


class FairGui(tk.Tk):
    def __init__(self, presenter: FairPresenter, data_path: Path) -> None:
        super().__init__()
        self.presenter = presenter
        self.title("Open Market Management GUI")
        self.geometry("1500x900")

        self._tables: dict[str, ttk.Treeview] = {}
        self._status_var = tk.StringVar(
            value=f"Data file: {data_path.resolve()}"
        )

        self._build_layout()
        self.refresh_state()

    def _build_layout(self) -> None:
        root_frame = ttk.Frame(self, padding=8)
        root_frame.pack(fill="both", expand=True)

        paned = ttk.Panedwindow(root_frame, orient="horizontal")
        paned.pack(fill="both", expand=True)

        state_frame = ttk.Frame(paned, padding=(0, 0, 8, 0))
        actions_frame = ttk.Frame(paned)
        paned.add(state_frame, weight=3)
        paned.add(actions_frame, weight=2)

        self._build_state_notebook(state_frame)
        self._build_actions_notebook(actions_frame)

        status = ttk.Label(
            root_frame,
            textvariable=self._status_var,
            anchor="w",
            padding=(4, 8, 4, 0),
        )
        status.pack(fill="x")

    def _build_state_notebook(self, parent: ttk.Frame) -> None:
        notebook = ttk.Notebook(parent)
        notebook.pack(fill="both", expand=True)

        self._tables["vendors"] = self._create_table_tab(
            notebook,
            "Traders",
            [
                ("vendor_id", "Trader ID", 110),
                ("name", "Name", 180),
                ("balance", "Balance", 110),
                ("stalls", "Stalls", 80),
            ],
        )
        self._tables["buyers"] = self._create_table_tab(
            notebook,
            "Buyers",
            [
                ("buyer_id", "Buyer ID", 110),
                ("name", "Name", 220),
            ],
        )
        self._tables["venues"] = self._create_table_tab(
            notebook,
            "Venues",
            [
                ("venue_id", "Venue ID", 110),
                ("name", "Name", 180),
                ("location", "Location", 220),
            ],
        )
        self._tables["stalls"] = self._create_table_tab(
            notebook,
            "Stalls",
            [
                ("stall_id", "Stall ID", 110),
                ("name", "Name", 160),
                ("fee", "Fee", 100),
                ("vendor_id", "Trader", 100),
                ("venue_id", "Venue", 100),
            ],
        )
        self._tables["products"] = self._create_table_tab(
            notebook,
            "Goods",
            [
                ("product_id", "Good ID", 110),
                ("name", "Name", 170),
                ("vendor_id", "Trader", 100),
                ("price", "Price", 100),
                ("quantity", "Quantity", 90),
            ],
        )
        self._tables["sales"] = self._create_table_tab(
            notebook,
            "Sales",
            [
                ("sale_id", "Sale ID", 110),
                ("product_id", "Good", 100),
                ("vendor_id", "Trader", 100),
                ("buyer", "Buyer", 140),
                ("quantity", "Qty", 70),
                ("unit_price", "Unit price", 100),
                ("total", "Total", 100),
                ("commission", "Commission", 100),
                ("timestamp", "Timestamp", 220),
            ],
        )
        self._tables["promotions"] = self._create_table_tab(
            notebook,
            "Promotions",
            [
                ("promotion_id", "Promotion ID", 120),
                ("message", "Message", 300),
                ("timestamp", "Timestamp", 220),
            ],
        )
        self._tables["attractions"] = self._create_table_tab(
            notebook,
            "Attractions",
            [
                ("attraction_id", "Attraction ID", 120),
                ("name", "Name", 170),
                ("description", "Description", 260),
                ("venue_id", "Venue", 100),
            ],
        )

        summary_frame = ttk.Frame(notebook, padding=8)
        self._summary_text = tk.Text(summary_frame, wrap="word", height=20)
        self._summary_text.pack(fill="both", expand=True)
        self._summary_text.configure(state="disabled")
        notebook.add(summary_frame, text="Summary")

    def _build_actions_notebook(self, parent: ttk.Frame) -> None:
        notebook = ttk.Notebook(parent)
        notebook.pack(fill="both", expand=True)

        market_tab = ttk.Frame(notebook, padding=8)
        participants_tab = ttk.Frame(notebook, padding=8)
        goods_tab = ttk.Frame(notebook, padding=8)
        reports_tab = ttk.Frame(notebook, padding=8)

        notebook.add(market_tab, text="Market")
        notebook.add(participants_tab, text="Participants")
        notebook.add(goods_tab, text="Goods & Sales")
        notebook.add(reports_tab, text="Reports")

        self._build_market_forms(market_tab)
        self._build_participant_forms(participants_tab)
        self._build_goods_forms(goods_tab)
        self._build_reports(reports_tab)

    def _build_market_forms(self, parent: ttk.Frame) -> None:
        parent.columnconfigure(0, weight=1)

        init_form = self._create_form(
            parent,
            "Initialize market",
            [
                ("name", "Name", ""),
                ("location", "Location", "Unknown"),
                ("commission", "Commission (%)", "0.00"),
            ],
            lambda payload: self.presenter.init_fair(
                payload["name"],
                payload["location"],
                payload["commission"],
            ),
            "Apply",
        )
        init_form.grid(row=0, column=0, sticky="ew", pady=(0, 8))

        advertise_form = self._create_form(
            parent,
            "Advertise event",
            [("message", "Message", "")],
            lambda payload: self.presenter.advertise_event(payload["message"]),
            "Create promotion",
        )
        advertise_form.grid(row=1, column=0, sticky="ew", pady=(0, 8))

        attraction_form = self._create_form(
            parent,
            "Add attraction",
            [
                ("name", "Name", ""),
                ("description", "Description", ""),
                ("venue_id", "Venue ID (optional)", ""),
            ],
            lambda payload: self.presenter.add_attraction(
                payload["name"],
                payload["description"],
                payload["venue_id"],
            ),
            "Create attraction",
        )
        attraction_form.grid(row=2, column=0, sticky="ew")

    def _build_participant_forms(self, parent: ttk.Frame) -> None:
        parent.columnconfigure(0, weight=1)
        parent.columnconfigure(1, weight=1)

        vendor_form = self._create_form(
            parent,
            "Add trader",
            [("name", "Name", "")],
            lambda payload: self.presenter.create_vendor(payload["name"]),
            "Create",
        )
        vendor_form.grid(row=0, column=0, sticky="ew", pady=(0, 8), padx=(0, 4))

        buyer_form = self._create_form(
            parent,
            "Add buyer",
            [("name", "Name", "")],
            lambda payload: self.presenter.create_buyer(payload["name"]),
            "Create",
        )
        buyer_form.grid(row=0, column=1, sticky="ew", pady=(0, 8), padx=(4, 0))

        venue_form = self._create_form(
            parent,
            "Add venue",
            [("name", "Name", ""), ("location", "Location", "Unknown")],
            lambda payload: self.presenter.create_venue(
                payload["name"], payload["location"]
            ),
            "Create",
        )
        venue_form.grid(row=1, column=0, sticky="ew", pady=(0, 8), padx=(0, 4))

        stall_form = self._create_form(
            parent,
            "Add stall",
            [
                ("name", "Name", ""),
                ("fee", "Fee", "0.00"),
                ("venue_id", "Venue ID (optional)", ""),
            ],
            lambda payload: self.presenter.create_stall(
                payload["name"],
                payload["fee"],
                payload["venue_id"],
            ),
            "Create",
        )
        stall_form.grid(row=1, column=1, sticky="ew", pady=(0, 8), padx=(4, 0))

        assign_form = self._create_form(
            parent,
            "Assign stall",
            [("stall_id", "Stall ID", ""), ("vendor_id", "Trader ID", "")],
            lambda payload: self.presenter.assign_stall(
                payload["stall_id"], payload["vendor_id"]
            ),
            "Assign",
        )
        assign_form.grid(row=2, column=0, columnspan=2, sticky="ew")

    def _build_goods_forms(self, parent: ttk.Frame) -> None:
        parent.columnconfigure(0, weight=1)
        parent.columnconfigure(1, weight=1)

        product_form = self._create_form(
            parent,
            "Add good",
            [
                ("vendor_id", "Trader ID", ""),
                ("name", "Name", ""),
                ("price", "Price", ""),
                ("quantity", "Quantity", ""),
            ],
            lambda payload: self.presenter.add_product(
                payload["vendor_id"],
                payload["name"],
                payload["price"],
                payload["quantity"],
            ),
            "Create",
        )
        product_form.grid(row=0, column=0, sticky="ew", pady=(0, 8), padx=(0, 4))

        sell_form = self._create_form(
            parent,
            "Sell",
            [
                ("product_id", "Good ID", ""),
                ("quantity", "Quantity", ""),
                ("buyer", "Buyer name", "Anonymous"),
            ],
            lambda payload: self.presenter.sell(
                payload["product_id"],
                payload["quantity"],
                payload["buyer"],
            ),
            "Record sale",
        )
        sell_form.grid(row=0, column=1, sticky="ew", pady=(0, 8), padx=(4, 0))

        trade_form = self._create_form(
            parent,
            "Trade (advanced)",
            [
                ("product_id", "Good ID", ""),
                ("quantity", "Quantity", ""),
                ("buyer", "Buyer name (optional)", ""),
                ("buyer_id", "Buyer ID (optional)", ""),
                ("price", "Negotiated price (optional)", ""),
            ],
            lambda payload: self.presenter.trade(
                payload["product_id"],
                payload["quantity"],
                payload["buyer"],
                payload["buyer_id"],
                payload["price"],
            ),
            "Record trade",
        )
        trade_form.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=(0, 8),
        )

        load_form = self._create_form(
            parent,
            "Load goods",
            [("product_id", "Good ID", ""), ("quantity", "Quantity", "")],
            lambda payload: self.presenter.load_goods(
                payload["product_id"], payload["quantity"]
            ),
            "Load",
        )
        load_form.grid(row=2, column=0, sticky="ew", padx=(0, 4))

        unload_form = self._create_form(
            parent,
            "Unload goods",
            [("product_id", "Good ID", ""), ("quantity", "Quantity", "")],
            lambda payload: self.presenter.unload_goods(
                payload["product_id"], payload["quantity"]
            ),
            "Unload",
        )
        unload_form.grid(row=2, column=1, sticky="ew", padx=(4, 0))

    def _build_reports(self, parent: ttk.Frame) -> None:
        parent.columnconfigure(0, weight=1)

        report_form = self._create_form(
            parent,
            "Vendor report",
            [("vendor_id", "Trader ID", "")],
            self._show_vendor_report,
            "Show",
        )
        report_form.grid(row=0, column=0, sticky="ew", pady=(0, 8))

        buttons = ttk.Frame(parent)
        buttons.grid(row=1, column=0, sticky="ew", pady=(0, 8))
        buttons.columnconfigure(0, weight=1)
        refresh_btn = ttk.Button(
            buttons,
            text="Refresh all views",
            command=lambda: self._run_action(lambda: "Views refreshed"),
        )
        refresh_btn.grid(row=0, column=0, sticky="ew")

        report_box_frame = ttk.LabelFrame(parent, text="Report output", padding=8)
        report_box_frame.grid(row=2, column=0, sticky="nsew")
        parent.rowconfigure(2, weight=1)

        self._report_text = tk.Text(report_box_frame, wrap="word", height=16)
        self._report_text.pack(fill="both", expand=True)
        self._report_text.configure(state="disabled")

    def _create_table_tab(
        self,
        notebook: ttk.Notebook,
        title: str,
        columns: list[tuple[str, str, int]],
    ) -> ttk.Treeview:
        frame = ttk.Frame(notebook, padding=8)

        column_ids = [item[0] for item in columns]
        table = ttk.Treeview(
            frame,
            columns=column_ids,
            show="headings",
            height=18,
        )
        for column_id, label, width in columns:
            table.heading(column_id, text=label)
            table.column(column_id, width=width, stretch=True, anchor="w")

        y_scroll = ttk.Scrollbar(frame, orient="vertical", command=table.yview)
        x_scroll = ttk.Scrollbar(frame, orient="horizontal", command=table.xview)
        table.configure(
            yscrollcommand=y_scroll.set,
            xscrollcommand=x_scroll.set,
        )

        table.grid(row=0, column=0, sticky="nsew")
        y_scroll.grid(row=0, column=1, sticky="ns")
        x_scroll.grid(row=1, column=0, sticky="ew")

        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)

        notebook.add(frame, text=title)
        return table

    def _create_form(
        self,
        parent: ttk.Frame,
        title: str,
        fields: list[tuple[str, str, str]],
        action: Callable[[dict[str, str]], str],
        button_text: str,
    ) -> ttk.LabelFrame:
        frame = ttk.LabelFrame(parent, text=title, padding=8)
        frame.columnconfigure(1, weight=1)

        values: dict[str, tk.StringVar] = {}
        for row_idx, (field_name, label, initial) in enumerate(fields):
            ttk.Label(frame, text=label).grid(
                row=row_idx,
                column=0,
                sticky="w",
                padx=(0, 8),
                pady=2,
            )
            var = tk.StringVar(value=initial)
            entry = ttk.Entry(frame, textvariable=var)
            entry.grid(row=row_idx, column=1, sticky="ew", pady=2)
            values[field_name] = var

        def on_submit() -> None:
            payload = {key: value.get() for key, value in values.items()}
            self._run_action(lambda: action(payload))

        submit = ttk.Button(frame, text=button_text, command=on_submit)
        submit.grid(
            row=len(fields),
            column=0,
            columnspan=2,
            sticky="ew",
            pady=(8, 0),
        )
        return frame

    def _show_vendor_report(self, payload: dict[str, str]) -> str:
        report = self.presenter.vendor_report_text(payload["vendor_id"])
        self._set_text(self._report_text, report)
        return "Vendor report updated"

    def _run_action(self, action: Callable[[], str]) -> None:
        try:
            message = action()
            self.refresh_state()
            self._status_var.set(message)
        except FairError as exc:
            self._status_var.set(f"Error: {exc}")
            messagebox.showerror("Operation failed", str(exc))

    def refresh_state(self) -> None:
        self._replace_rows("vendors", self.presenter.vendors_rows())
        self._replace_rows("buyers", self.presenter.buyers_rows())
        self._replace_rows("venues", self.presenter.venues_rows())
        self._replace_rows("stalls", self.presenter.stalls_rows())
        self._replace_rows("products", self.presenter.products_rows())
        self._replace_rows("sales", self.presenter.sales_rows())
        self._replace_rows("promotions", self.presenter.promotions_rows())
        self._replace_rows("attractions", self.presenter.attractions_rows())
        self._set_text(self._summary_text, self.presenter.summary_text())

    def _replace_rows(self, table_name: str, rows: list[tuple[str, ...]]) -> None:
        table = self._tables[table_name]
        children = table.get_children()
        if children:
            table.delete(*children)
        for row in rows:
            table.insert("", "end", values=row)

    def _set_text(self, widget: tk.Text, value: str) -> None:
        widget.configure(state="normal")
        widget.delete("1.0", "end")
        widget.insert("1.0", value)
        widget.configure(state="disabled")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Open market management GUI")
    parser.add_argument(
        "--data",
        default=DEFAULT_DATA_FILE,
        help="Path to JSON data file.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    presenter = FairPresenter.from_path(Path(args.data))
    app = FairGui(presenter, Path(args.data))
    app.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
