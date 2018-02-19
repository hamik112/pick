const USER_ID = 'userid'
const USER_NAME = 'username'
const USER_IMAGE = 'userimage'
const USER_EMAIL = 'useremail'

export function setUserId (userId) {
  localStorage.setItem(USER_ID, userId)
}

export function getUserId () {
  return localStorage.getItem(USER_ID)
}

export function clearUserId () {
  localStorage.removeItem(USER_ID)
}

export function setUserName (userName) {
  localStorage.setItem(USER_NAME, userName)
}

export function getUserName () {
  return localStorage.getItem(USER_NAME)
}

export function clearUserName () {
  localStorage.removeItem(USER_NAME)
}

export function setUserImage (userImage) {
  localStorage.setItem(USER_IMAGE, userImage)
}

export function getUserImage () {
  return localStorage.getItem(USER_IMAGE)
}

export function clearUserImage () {
  localStorage.removeItem(USER_IMAGE)
}

export function setUserEmail (userEmail) {
  localStorage.setItem(USER_EMAIL, userEmail)
}

export function getUserEmail () {
  return localStorage.getItem(USER_EMAIL)
}

export function clearUserEmail () {
  localStorage.removeItem(USER_EMAIL)
}

export function isLoggedIn () {
  if (getUserId()) {
    return true
  }
  return false
}

export function requireAuth (to, from, next) {
  if (!isLoggedIn()) {
    next({
      // path: '/',
      // query: { redirect: to.fullPath }
    })
  } else {
    next()
  }
}
