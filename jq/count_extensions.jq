map(select(.progress.type == "real"))
| map(.progress.extension)
| reduce .[] as $ext ({}; .[$ext] += 1)
| to_entries
| sort_by(-.value)
| from_entries
