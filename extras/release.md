# Making a release

- Update version in `setup.py`
- Update version in `docs/conf.py`
- Update version in `restic_compose_backup/__init__.py`
- Build and tag image
- push: `docker push zettaio/restic-compose-backup:<version>`
- Ensure RTD has new docs published

## Example

When releasing a bugfix version we need to update the
main image as well.

```bash
docker build src --tag zettaio/restic-compose-backup:0.3
docker build src --tag zettaio/restic-compose-backup:0.3.3

docker push zettaio/restic-compose-backup:0.3
docker push zettaio/restic-compose-backup:0.3.3
```
