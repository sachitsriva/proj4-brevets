# Brevet Calculator

Calculates checkpoint opening and closing times using Flask and Ajax. Select the brevet distance and starting time, then enter checkpoint distances.

## Rules

| Segment | Opening speed | Closing speed |
|---|---:|---:|
| 0–200 km | 34 km/h | 15 km/h |
| 200–400 km | 32 km/h | 15 km/h |
| 400–600 km | 30 km/h | 15 km/h |
| 600–1000 km | 28 km/h | 11.428 km/h |

(Segment times are added and rounded to the nearest minute.)

Official calculation rules: https://rusa.org/pages/acp-brevet-control-times-calculator

## Run

Fill in `brevets/credentials.ini`, then:

```bash
cd brevets
docker build -t brevets .
docker run --rm -p 5000:5000 brevets
```

Open http://localhost:5000.

## Tests (Five Tests)

From `brevets`, with dependencies installed:

```bash
nosetests -v
```

## Author

Sachit Srivastava (sachit@uoregon.edu)
