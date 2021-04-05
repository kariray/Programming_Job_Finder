import csv


def save_to_file(jobs, name):
    file = open(f"{name}.csv", mode="w")
    writer = csv.writer(file)
    writer.writerow(["title", "company", "Apply_link"])
    for job in jobs:
        writer.writerow(list(job.values())[0:3])
    return
