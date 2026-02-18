const OPS = ['KA','NA','TA','STA','PA','SI','SA','SO','SON','SIN','MA','TAN','N\'','N\'KA','KI','KE','EL','LA','BA','NAN','BU','U','BO','KU','I','E','DI'];

export function validateNtopy4(text) {
  const tokens = (text || '').toUpperCase().split(/\s+/);
  return tokens.some((token) => OPS.includes(token));
}
