export function statusMapping(status) {
  if (status == "wait pay") {
    return "arrearage";
  } else if (status == "delivering") {
    return "delivering";
  } else if (status == "done") {
    return "complete";
  } else {
    return "can't decode status";
  }
}
