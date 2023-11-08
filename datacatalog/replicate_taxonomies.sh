LOCATION_SOURCE=us
LOCATION_TARGETS="southamerica-west1 southamerica-east1"
FILE_NAME=taxonomies

read -p "CAUTION - Do you want to replicate taxonomies from $LOCATION_SOURCE to $LOCATION_TARGETS? (y/n) " proceed

if [[ "$proceed" != "y" ]]; then
  echo "Replication canceled."
else
  echo "Replicating taxonomies from $LOCATION_SOURCE..."
  for LOCATION_TARGET in $LOCATION_TARGETS; do
    TAXONOMIES=$( gcloud data-catalog taxonomies list --location=$LOCATION_SOURCE | grep -oP '/taxonomies/\K[^/]+' | paste -sd, -)
    # Export taxonomies
    gcloud data-catalog taxonomies export $TAXONOMIES --location=$LOCATION_SOURCE > "$FILE_NAME.$LOCATION_SOURCE.yaml"

    # Delete taxonomies - not exists

    # Create taxonomies
    gcloud data-catalog taxonomies import "$FILE_NAME.$LOCATION_SOURCE.yaml" --location="$LOCATION_TARGET" > "$FILE_NAME.$LOCATION_TARGET.yaml"

    echo "Replicated from $LOCATION_SOURCE to $LOCATION_TARGET, review file $FILE_NAME.$LOCATION_TARGET.yaml for details"
done
fi

