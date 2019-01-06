import * as util from './util';

interface ChangeRequest {
  current_password: string;
  new_password: string;
}

const change = async (data: ChangeRequest): Promise<object> => {
  const res = await util.sendRequest(util.Methods.Post, '/password/', data);
  if (res.status >= 400) {
    throw await res.json();
  }
  if (res.status === 204) {
    return {};
  }
  return await res.json();
};

export const changePassword = async (currentPassword: string, newPassword: string): Promise<boolean> => {
  const req: ChangeRequest = { current_password: currentPassword, new_password: newPassword };
  return change(req)
    .then(res => {
      return true;
    })
    .catch(errJson => {
      return false;
    });
};

interface ResetRequest {
  email: string;
}

interface ResetResponse {}

const reset = async (data: ResetRequest): Promise<ResetResponse> => {
  const res = await util.sendRequest(util.Methods.Post, '/password/reset/', data, false);
  if (res.status >= 400) {
    throw await res.json();
  }
  if (res.status === 204) {
    return {};
  }
  return await res.json();
};

export const resetPassword = async (email: string): Promise<boolean> => {
  const req: ResetRequest = { email };
  return reset(req)
    .then(res => {
      return true;
    })
    .catch(errJson => {
      return false;
    });
};

interface ResetConfirmRequest {
  uid: string;
  token: string;
  new_password: string;
}

interface ResetConfirmResponse {}

const resetConfirm = async (data: ResetConfirmRequest): Promise<ResetConfirmResponse> => {
  const res = await util.sendRequest(util.Methods.Post, '/password/reset/confirm/', data, false);
  if (res.status >= 400) {
    throw await res.json();
  }
  if (res.status === 204) {
    return {};
  }
  return await res.json();
};

export const confirmNewPassword = async (uid: string, token: string, newPassword: string): Promise<boolean> => {
  const req: ResetConfirmRequest = { uid, token, new_password: newPassword };
  return resetConfirm(req)
    .then(res => {
      return true;
    })
    .catch(errJson => {
      return false;
    });
};
