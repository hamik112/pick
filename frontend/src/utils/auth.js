const USER_ID = 'userid'

export function setUserId (userId) {
  localStorage.setItem(USER_ID, userId)
}

export function getUserId () {
  return localStorage.getItem(USER_ID)
}

export function clearUserId () {
  localStorage.removeItem(USER_ID)
}

export function isLoggedIn () {
  if (getUserId()) {
    return true
  }
  return false
}

export function requireAuth (to, from, next) {
  // if (!isLoggedIn()) {
  //   next({
  //     path: '/',
  //     query: { redirect: to.fullPath }
  //   })
  // } else {
  // }
    next()
}
