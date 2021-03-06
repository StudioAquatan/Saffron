import * as util from '../util';

describe('isIntStr', () => {
  it('correct', () => {
    expect(util.isIntStr('123')).toBe(true);
  });
  it('words', () => {
    expect(util.isIntStr('hoge')).toBe(false);
  });
  it('include words', () => {
    expect(util.isIntStr('hoge123')).toBe(false);
    expect(util.isIntStr('123hoge')).toBe(false);
    expect(util.isIntStr('h1o2g3e')).toBe(false);
  });
  it('no word', () => {
    expect(util.isIntStr('')).toBe(false);
  });
});

describe('isFloatStr', () => {
  it('correct', () => {
    expect(util.isFloatStr('1.23')).toBe(true);
    expect(util.isFloatStr('-1.23')).toBe(true);
  });
  it('words', () => {
    expect(util.isFloatStr('hoge')).toBe(false);
  });
  it('include words', () => {
    expect(util.isFloatStr('hoge123')).toBe(false);
    expect(util.isFloatStr('123hoge')).toBe(false);
    expect(util.isFloatStr('h1o2g3e')).toBe(false);
  });
  it('no word', () => {
    expect(util.isFloatStr('')).toBe(false);
  });
  it('int', () => {
    expect(util.isFloatStr('10')).toBe(true);
  });
});

describe('deleteNullObj', () => {
  it('correct', () => {
    const data = {
      hoge: 'hoge',
      foo: null,
    };
    const want = {
      hoge: 'hoge',
    };
    expect(util.deleteNullObj(data)).toEqual(want);
  });
  it('have nest', () => {
    const data = {
      hoge: 'hoge',
      foo: {
        piyo: null,
      },
      fuga: {
        a: 100,
        b: null,
      },
    };
    const want = {
      hoge: 'hoge',
      fuga: {
        a: 100,
      },
    };
    expect(util.deleteNullObj(data)).toEqual(want);
  });
});
