import * as util from './util';

interface CreateRequest {
  username: string;
  password: string;
  screenName: string | null;
  gpa: number | null;
}

interface CreateResponse {
  pk: number;
  username: string;
  email: string;
  screenName: string;
  non_field_errors: string[];
}

const create = async (data: CreateRequest): Promise<CreateResponse> => {
  const res = await util.sendRequest(util.Methods.Post, '/users/create/', data, false);
  if (res.status >= 400) {
    throw await res.json();
  }
  return await res.json();
};

export const createUser = async (username: string, password: string): Promise<boolean> => {
  const req: CreateRequest = { username, password, screenName: null, gpa: null };
  return create(req)
    .then(res => {
      return true;
    })
    .catch(errJson => {
      // TODO: errJson(エラーメッセージ)を活用する
      return false;
    });
};

interface ActivateRequest {
  uid: string;
  token: string;
}

interface ActivateResponse {}

const activate = async (data: ActivateRequest): Promise<ActivateResponse> => {
  const res = await util.sendRequest(util.Methods.Post, '/users/activate/', data, false);
  if (res.status >= 400) {
    throw await res.json();
  }
  if (res.status === 204) {
    return {};
  }

  return await res.json();
};

export const activateUser = async (uid: string, token: string): Promise<boolean> => {
  const req: ActivateRequest = { uid, token };
  return activate(req)
    .then(res => {
      return true;
    })
    .catch(errJson => {
      return false;
    });
};

interface GetMeResponse {}

const getMe = async (): Promise<GetMeResponse> => {
  const res = await util.sendRequest(util.Methods.Get, '/users/me/', {});
  if (res.status >= 400) {
    throw await res.json();
  }
  return await res.json();
};

export const getMeInfo = async (): Promise<GetMeResponse> => {
  return getMe().then(res => {
    return res;
  });
};
