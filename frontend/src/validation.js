export const MAX_EMAIL_LENGTH = 255;
export const MAX_PHONE_LENGTH = 20;

// Kept in step with backend/validation.py so the browser and the API agree.
export const EMAIL_PATTERN =
  /^[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+)*@[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)*\.[A-Za-z]{2,63}$/;
export const PHONE_PATTERN = /^\+?(?:\([0-9]{1,6}\)\s?)?[0-9][0-9\s().-]{3,17}[0-9]$/;

export function isValidEmail(value) {
  const email = String(value ?? '').trim();
  return email.length <= MAX_EMAIL_LENGTH && EMAIL_PATTERN.test(email);
}

export function isValidPhone(value) {
  const phone = String(value ?? '').trim();
  if (phone.length > MAX_PHONE_LENGTH || !PHONE_PATTERN.test(phone)) return false;
  const digits = (phone.match(/\d/g) || []).length;
  return digits >= 7 && digits <= 15;
}
