export const rules = {
  required: (value) => !!value || "required",
  arrayRequired: (v) => {
    return v.length > 0 || "required";
  },
  name: (v) => {
    return (
      (v != null && v.length >= 3 && v.length <= 50) ||
      "Must be between 3-50 characters"
    );
  },
  roomName: (v) => {
    return (v != null && v.length <= 25) || "Input at most 25 characters";
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
  phoneNumber: (v) => {
    return (
      (v != null && v.length >= 9 && v.length <= 15) ||
      "Must be between 9-15 numbers"
    );
  },
  password: (v) => {
    return (
      (v != null && v.length >= 6 && v.length <= 30) ||
      "Must be between 6-30 characters"
    );
  },
  address: (v) => {
    return (v != null && v.length <= 50) || "Must be between 6-50 characters";
  },
  description: (v) => {
    return (v != null && v.length <= 300) || "Input at most300 characters";
  },
  cost: (v) => {
    return (
      (v != null && v > 0 && v <= 20000) ||
      "Please enter a positive integer within 20000"
    );
  },
  files: (v) => {
    return v.length <= 8 || "Uploads at most 8 images";
  },
};
