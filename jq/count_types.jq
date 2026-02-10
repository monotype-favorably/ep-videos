{
    "not found": map(select(.progress.type == "attempts")) | length,
    "found": map(select(.progress.type == "real")) | length,
    "downloaded": map(select(.progress.downloaded? == true)) | length
}
