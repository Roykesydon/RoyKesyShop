export const rules = {
  required: (value) => !!value || "required",
  arrayRequired: (v) => {
    return v.length > 0 || "required";
  },
  id: (v) => {
    return (
      (v != null && v.length >= 3 && v.length <= 50) ||
      "Must be between 3-50 characters"
    );
  },
  emailFormat: (value) => {
    const pattern =
      /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return (value != null && pattern.test(value)) || "email format error";
  },
  emailLength: (v) => {
    return (
      (v != null && v.length >= 3 && v.length <= 50) ||
      "Must be between 3-50 characters"
    );
  },
  password: (v) => {
    return (
      (v != null && v.length >= 6 && v.length <= 30) ||
      "Must be between 6-30 characters"
    );
  },
  title: (v) => {
    return (
      (v != null && v.length >= 2 && v.length <= 50) ||
      "Must be between 2-50 characters"
    );
  },
  description: (v) => {
    return (v != null && v.length <= 500) || "Input at most 500 characters";
  },
  cost: (v) => {
    return (
      (v != null && v > 0 && v <= 1000000) ||
      "Please enter a positive integer within 1000000"
    );
  },
  files: (v) => {
    return v.length > 0 || "Please uplaod picture";
  },
  parentClass: (v) => {
    return (
      (v != null && v.length >= 1 && v.length <= 25) ||
      "Must be between 1-25 characters"
    );
  },
  subClass: (v) => {
    return (
      (v != null && v.length >= 1 && v.length <= 25) ||
      "Must be between 1-25 characters"
    );
  },
};
