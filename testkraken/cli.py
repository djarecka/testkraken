"""Command-line interface for Testkraken."""

import click
import sys

from testkraken.workflowregtest import WorkflowRegtest

def _pdb_excepthook(type, value, tb):
    import traceback

    traceback.print_exception(type, value, tb)
    print()
    if sys.stdin.isatty() and sys.stdout.isatty() and sys.stderr.isatty():
        import pdb
        pdb.post_mortem(tb)

@click.command()
@click.argument("path", type=click.Path(exists=True))
@click.option(
    "-w",
    "--working-dir",
    type=click.Path(),
    help="Working directory of workflow. Default is a temporary directory.",
)
@click.option(
    "--pdb",
    is_flag=True,
    help="Fall into pdf debugging mode if unhandled exception happens.",
)
def main(path, working_dir=None, tmp_working_dir=True, pdb=False):
    """This script runs the workflow in PATH."""
    if pdb:
        sys.excepthook = _pdb_excepthook
    if working_dir:
        tmp_working_dir = False
    wf = WorkflowRegtest(
        workflow_path=path, working_dir=working_dir, tmp_working_dir=tmp_working_dir
    )
    print(f"\n running testkraken for {path}; working directory - {working_dir}")
    wf.run()
    wf.merge_outputs()
    wf.dashboard_workflow()
