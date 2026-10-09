const params = new URL(location.href).searchParams;
if (!params.get("week")) {
    // TODO: load week data from local storage
    location.href = location.pathname + "?week=0";
}
