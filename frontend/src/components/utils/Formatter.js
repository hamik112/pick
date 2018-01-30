export function dateFormatter (str) {
  // YYYY-MM-DD HH:MM:SS
  const dt = new Date(str)
  const mm = dt.getMonth() + 1
  const dd = dt.getDate()
  const YYYYMMDD = [dt.getFullYear(), (mm > 9 ? '' : '0') + mm, (dd > 9 ? '' : '0') + dd].join('-')
  const HHMMSS = [dt.getHours(), dt.getMinutes(), dt.getSeconds()].join(':')

  return YYYYMMDD + ' ' + HHMMSS
}

export function numberFormatter (num) {
  return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',')
}


export function numberToFixed(num,cut) {
	return num.toFixed(cut)
}