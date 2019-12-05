# Making a release

- Update version in `setup.py`
- Update version in `docs/conf.py`
- Build and tag image
- push: `docker push zettaio/restic-compose-backup:<version>`
- Ensure RTD has new docs published

## Example

When releasing a bugfix version we need to update the
main image as well.

```bash
docker build . --tag zettaio/restic-compose-backup:0.3
docker build . --tag zettaio/restic-compose-backup:0.3.1

docker push zettaio/restic-compose-backup:0.3
docker push zettaio/restic-compose-backup:0.3.1
```
