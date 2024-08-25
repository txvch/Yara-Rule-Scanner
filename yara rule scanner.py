import os
import yara
import concurrent.futures
from rich.console import Console
from rich.live import Live
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
import platform
import subprocess
import time

console = Console()

system_name = platform.system()
if system_name == "Windows":
    subprocess.run("cls", shell=True)
else:
    subprocess.run("clear", shell=True)

try:
    rules = yara.compile(filepath='yara.yar')
except yara.SyntaxError as e:
    console.print(f"[bold red]Error compiling YARA rules:[/bold red] {e}")
    rules = None
except Exception as e:
    console.print(f"[bold red]Unexpected error:[/bold red] {e}")
    rules = None

matches = []
file_count = 0
error_count = 0
start_time = time.time()

progress = Progress(
    SpinnerColumn(),
    TextColumn("[progress.description]{task.description}"),
    BarColumn(),
    TextColumn("[cyan]{task.fields[file_count]}[/cyan] files scanned, [bold red]{task.fields[error_count]}[/bold red] errors"),
    TextColumn("[bold blue]{task.fields[elapsed_time]:.2f}[/bold blue] seconds elapsed"),
    console=console,
)

task = progress.add_task("[cyan]Scanning files...", total=None, file_count=0, error_count=0, elapsed_time=0)

with Live(progress, console=console, refresh_per_second=10):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for root, _, files in os.walk('directory_to_scan'):
            for file in files:
                file_path = os.path.join(root, file)
                futures.append(executor.submit(lambda p: (p, rules.match(data=open(p, 'rb').read())), file_path))

        for future in concurrent.futures.as_completed(futures):
            file_path, match = future.result()
            file_count += 1
            if match is None:
                error_count += 1
            else:
                if match:
                    matches.append((file_path, match))

            elapsed_time = time.time() - start_time
            progress.update(task, advance=1, file_count=file_count, error_count=error_count, elapsed_time=elapsed_time)

progress.update(task, total=file_count, file_count=file_count)

console.print(f"\n[bold green]Scan complete![/bold green] [yellow]{file_count}[/yellow] files scanned, [bold red]{error_count}[/bold red] errors.\n")
console.print(f"[bold blue]Elapsed time:[/bold blue] {elapsed_time:.2f} seconds\n")

if matches:
    table = Table(title="YARA Matches", show_lines=True)
    table.add_column("File Path", style="dim", width=60)
    table.add_column("Rule Names", style="bold magenta")

    for file_path, match in matches:
        rule_names = ", ".join([rule.rule for rule in match])
        table.add_row(file_path, rule_names)

    console.print(table)
else:
    console.print("[bold green]No matches found.[/bold green]")

console.print(Panel(Text("🔍 YARA File Scanner 🔍\n\nFast and Efficient File Scanning", justify="center", style="bold cyan"), title="Welcome", border_style="bright_yellow"))

if rules:
    script_directory = os.path.dirname(os.path.abspath(__file__))
    yara_rule_file = os.path.join(script_directory, 'yara.yar')
    scan_directory_path = console.input("[bold yellow]Enter the directory to scan:[/bold yellow] ").strip()
    start_time = time.time()
    matches, total_files, error_count = None, file_count, error_count
    end_time = time.time()
    elapsed_time = end_time - start_time
    console.print(f"\n[bold green]Scan complete![/bold green] [yellow]{total_files}[/yellow] files scanned, [bold red]{error_count}[/bold red] errors.\n")
    console.print(f"[bold blue]Elapsed time:[/bold blue] {elapsed_time:.2f} seconds\n")
    if matches:
        table = Table(title="YARA Matches", show_lines=True)
        table.add_column("File Path", style="dim", width=60)
        table.add_column("Rule Names", style="bold magenta")
        for file_path, match in matches:
            rule_names = ", ".join([rule.rule for rule in match])
            table.add_row(file_path, rule_names)
        console.print(table)
    else:
        console.print("[bold green]No matches found.[/bold green]")
