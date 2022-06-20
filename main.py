import concurrent.futures
import multiprocessing as mp
import platform
import time
import sys
import os

ALL_CORES = os.cpu_count()
FOUR_PROCESSES = 4
ONE_THREAD = 1
FOUR_THREADS = 4
args = [15972490, 80247910, 92031257, 75940266,
        97986012, 87599664, 75231321, 11138524,
        68870499, 11872796, 79132533, 40649382,
        63886074, 53146293, 36914087, 62770938]


def summation(num):
    result = 0
    for i in range(1, num + 1):
        result += (num - i) * i
    return result


def print_time(start, end):
    return format((end-start)*2, '.3f')


def run_processes(number_of_processes):
    start = time.perf_counter()
    process_pool = mp.Pool(processes=number_of_processes)
    process_pool.map(summation, args)
    end = time.perf_counter()
    return print_time(start, end)


def run_thread(number_of_threads):
    start = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=number_of_threads) as executor:
        executor.map(summation, args)
    end = time.perf_counter()
    return print_time(start, end)


def run_multiple(func, arg, times):
    return [func(arg) for _ in range(times)]


def median(length):
    return int((length + 1) / 2)


def generate_report_html():
    python_version = platform.python_version()
    python_compiler = platform.python_implementation()
    interpreter_version = sys.version
    os_system = platform.version()
    system = platform.system()
    processor = platform.processor()
    cores = os.cpu_count()

    html_file = open("report.html", 'w')

    body = f"""
        <!DOCTYPE html>
            <head>
                <style>
                    body {{font-family: "Times New Roman", Times, serif;backgroundColor:#edf2ef}}
                    table {{width:100%;}}
                    table, th, td {{border: 1px solid black;border-collapse: collapse;}}
                    th, td {{padding: 10px;margin: 0 auto; text-align:center}}
                    tr:nth-child(even) {{background-color: #eee;}}
                    tr:nth-child(odd) {{background-color: #fff;}}
                    th {{background-color: #fff;color: black;}}
                    h5 {{margin: 0 auto}}
                    #sign {{font-size:15px; margin: 25px 0px}}
                    #caption-style {{font-size: 14px; text-align:left}}
                </style>
            </head>
            <body>
                <h2>Multithreading/Multiprocessing benchmark results</h2>
                <h3>Execution environment</h3>
                <h5>Python Version: {python_version}</h5>
                <h5>Interpreter: {python_compiler}</h5>
                <h5>Interpreter version: {interpreter_version}</h5>
                <h5>Operating System: {system}</h5>
                <h5>Operating System Version: {os_system}</h5>
                <h5>Processor Version: {processor}</h5>
                <h5>Number of CPUs: {cores}</h5>
                <h3>Test results<h3>
                <table>
                    <caption id="caption-style">The following table shows detailed test results:</caption>
                    {generate_table_details(oneThreadTimes, fourThreadTimes, fourProcessTimes, allProcessTimes)}
                <table>
                <h3>Summary</h3>
                <table>
                    <caption id="caption-style">The following table shows the median of all results:</caption>
                    {generate_median_results(oneThreadMedian, fourThreadMedian, fourProcessMedian, allProcessMedian)}
                <table>
                <footer>
                    <div id="sign">App author: Tomasz Luczynski</p>
                </footer>
            </body>
        </html>
    """
    html_file.write(body)
    html_file.close()


def generate_table_details(one, two, three, four):
    table = """
            <tr>
                <th>Execution</th>
                <th>1 Thread (s)</th>
                <th>4 Thread (s)</th>
                <th>4 Processes (s)</th>
                <th>Processes Based on Number of CPU(s)</th>
              </tr>
            """
    for i in range(5):
        table += f"""
                <tr>
                     <td>{i}</td>
                     <td>{one[i]}</td>
                     <td>{two[i]}</td>
                     <td>{three[i]}</td>
                     <td>{four[i]}</td>
                </tr>
            """
    return table


def generate_median_results(one, two, three, four):
    return f"""
            <tr>
                <th>Execution</th>
                <th>1 Thread (s)</th>
                <th>4 Thread (s)</th>
                <th>4 Processes (s)</th>
                <th>Processes Based on Number of CPU(s)</th>
              </tr>
              
            <tr>
                <td>Median</td>
                <td>{one}</td>
                <td>{two}</td>
                <td>{three}</td>
                <td>{four}</td>
            </tr>
    """


if __name__ == '__main__':
    program_start = time.perf_counter()
    fourProcessTimes = run_multiple(run_processes, FOUR_PROCESSES, 5)
    allProcessTimes = run_multiple(run_processes, ALL_CORES, 5)
    oneThreadTimes = run_multiple(run_thread, ONE_THREAD, 5)
    fourThreadTimes = run_multiple(run_thread, FOUR_THREADS, 5)

    fourProcessTimes.sort()
    allProcessTimes.sort()
    oneThreadTimes.sort()
    fourThreadTimes.sort()

    fourProcessMedian = fourProcessTimes[median(5)]
    allProcessMedian = allProcessTimes[median(5)]
    oneThreadMedian = oneThreadTimes[median(5)]
    fourThreadMedian = fourThreadTimes[median(5)]

    generate_report_html()

    print(fourProcessTimes)
    print(allProcessTimes)
    print(oneThreadTimes)
    print(fourThreadTimes)

    program_end = time.perf_counter()
    print(f"Finished in {program_end-program_start} seconds.")
