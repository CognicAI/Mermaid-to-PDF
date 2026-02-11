# GitHub Actions CI/CD Workflows

This directory contains automated workflows for the Documentation Pipeline project.

## Workflows

### 1. Docker Build and Test (`docker.yml`)

**Triggers:**
- Push to `main` or `develop` branches
- Pull requests to `main` branch
- Manual workflow dispatch

**Jobs:**

#### `build-and-test`
- **Purpose**: Build Docker image and test basic functionality
- **Steps**:
  1. Checkout code
  2. Set up Docker Buildx for caching
  3. Build Docker image with GitHub Actions cache
  4. Verify image was created successfully
  5. Create output directories
  6. Test pipeline with README.md
  7. Verify PDF generation
  8. Upload PDF and markdown artifacts
  9. Generate job summary

**Artifacts**: Generated PDFs and processed markdown files (retained for 30 days)

#### `test-custom-paths`
- **Purpose**: Test custom path functionality (v2.0 feature)
- **Steps**:
  1. Build Docker image
  2. Create test directory structure (`/tmp/test-docs/markdown`)
  3. Generate test markdown file
  4. Run pipeline with custom path mount
  5. Verify PDF generation from custom path
  6. Upload test results

**Artifacts**: Custom path test PDFs (retained for 7 days)

#### `lint-dockerfile`
- **Purpose**: Lint Dockerfile for best practices
- **Tool**: Hadolint
- **Threshold**: Warning level

## Key Features

### Build Caching
The workflow uses GitHub Actions cache to speed up Docker builds:
```yaml
cache-from: type=gha
cache-to: type=gha,mode=max
```

### Image Loading
Critical fix for the "image not found" error:
```yaml
load: true  # Ensures image is loaded into Docker daemon
```

### Verification Steps
Each workflow includes verification to catch failures early:
- Image verification after build
- PDF generation verification
- File existence checks

### Job Summary
The workflow generates a summary visible in the Actions tab showing:
- Build status
- Generated files
- File sizes

## Troubleshooting CI/CD Issues

### Error: "Unable to find image 'docs-pipeline:latest'"

**Cause**: Docker image wasn't loaded into the daemon after building.

**Solution**: Ensure `load: true` is set in `docker/build-push-action`:
```yaml
- name: Build Docker image
  uses: docker/build-push-action@v5
  with:
    load: true  # This is critical!
    tags: docs-pipeline:latest
```

### Error: "pull access denied for docs-pipeline"

**Cause**: Docker is trying to pull from Docker Hub instead of using local build.

**Solution**: 
1. Verify the build step completes successfully
2. Add image verification step to confirm build
3. Use exact tag `docs-pipeline:latest` in run commands

### Build Takes Too Long

**Solution**: Utilize caching:
```yaml
cache-from: type=gha
cache-to: type=gha,mode=max
```

First build: ~10-20 minutes  
Cached builds: ~2-5 minutes

### Custom Path Tests Fail

**Causes**:
- Incorrect volume mount syntax
- Path doesn't exist in runner
- Permission issues

**Solution**:
- Use absolute paths in Linux runners: `/tmp/test-docs`
- Ensure directories are created before mounting
- Use `:ro` (read-only) for input mounts

## Local Testing

Test the workflow locally before pushing:

```bash
# Simulate the build step
docker build -t docs-pipeline:latest .

# Verify image exists
docker images | grep docs-pipeline

# Test with README
docker run --rm \
  -v $(pwd):/app/input:ro \
  -v $(pwd)/output:/app/output \
  docs-pipeline:latest python3 main.py /app/input/README.md

# Test custom path
mkdir -p /tmp/test-docs
echo "# Test" > /tmp/test-docs/test.md
docker run --rm \
  -v /tmp/test-docs:/app/input:ro \
  -v $(pwd)/output:/app/output \
  docs-pipeline:latest python3 main.py /app/input/test.md
```

## Adding New Workflows

When adding new workflows:

1. **Always include image verification**:
   ```yaml
   - name: Verify Docker image
     run: docker images | grep docs-pipeline
   ```

2. **Use the `load: true` parameter**:
   ```yaml
   - name: Build Docker image
     uses: docker/build-push-action@v5
     with:
       load: true
   ```

3. **Add verification steps**:
   ```yaml
   - name: Verify output
     run: |
       if [ ! -f expected-output.pdf ]; then
         exit 1
       fi
   ```

4. **Upload artifacts for debugging**:
   ```yaml
   - name: Upload artifacts
     uses: actions/upload-artifact@v4
     if: always()  # Upload even on failure
   ```

## Best Practices

1. **Fail Fast**: Add verification after each critical step
2. **Cache Everything**: Use GitHub Actions cache for Docker layers
3. **Upload Artifacts**: Always upload outputs for debugging
4. **Job Summaries**: Add summaries for better visibility
5. **Test Custom Paths**: New feature - ensure it's tested in CI
6. **Lint Dockerfiles**: Catch issues before runtime
7. **Parallel Jobs**: Run independent tests in parallel

## Monitoring

**Check workflow runs**: 
- GitHub repo → Actions tab
- View job summaries for quick status
- Download artifacts for verification

**Typical run times**:
- First build: 10-20 minutes
- Cached builds: 2-5 minutes  
- Custom path tests: 1-2 minutes
- Total workflow: 15-25 minutes (first run)

## References

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Build Push Action](https://github.com/docker/build-push-action)
- [Hadolint](https://github.com/hadolint/hadolint)
