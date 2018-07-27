import {
  LOGIN,
  LOGOUT,
} from './types';

export const login = (token) => {
  return {
    type: LOGIN,
    token: token,
  };
};

export const logout = () => {
  return {
    type: LOGOUT,
  };
};
