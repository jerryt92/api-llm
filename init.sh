project_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
echo "project_dir: $project_dir"
export PYTHONPATH="$project_dir:$PYTHONPATH"