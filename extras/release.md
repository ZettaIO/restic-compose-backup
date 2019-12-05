# Making a release

- Update version in setup.py
- Build and tag image
- push: `docker push zettaio/restic-compose-backup:<version>`
- Ensure RTD has new docs published

## Example

```bash
docker build . --tag zettaio/restic-compose-backup:0.2.0
docker push zettaio/restic-compose-backup:0.2.0
```
