import { Button, Card, CardContent, FormControl, FormHelperText, Grid, Input, InputLabel } from '@material-ui/core';
import * as React from 'react';
import { RouteComponentProps } from 'react-router';

import { resetPassword } from '../api/password';
import PopUp from './PopUp';

interface PasswordResetProps extends RouteComponentProps<any> {}

interface PasswordResetState {
  email: string;
  passwordResetErrMsg: string;
  showPopUp: boolean;
}

class PasswordReset extends React.Component<PasswordResetProps, PasswordResetState> {
  constructor(props: PasswordResetProps) {
    super(props);
    this.state = {
      email: '',
      passwordResetErrMsg: '',
      showPopUp: false,
    };

    this.handleChangeUsername = this.handleChangeUsername.bind(this);
    this.handleClickPasswordReset = this.handleClickPasswordReset.bind(this);
    this.handleClosePopUp = this.handleClosePopUp.bind(this);
  }

  public handleChangeUsername(e: React.ChangeEvent<HTMLInputElement>) {
    e.preventDefault();
    this.setState({ email: e.target.value });
  }

  public handleClickPasswordReset() {
    resetPassword(this.state.email).then(success => {
      if (!success) {
        this.setState({ passwordResetErrMsg: 'メール送信に失敗しました' });
        return;
      }
      this.setState({ showPopUp: true });
    });
  }

  public handleKeyPress(e: React.KeyboardEvent<HTMLInputElement>) {
    if (e.which === 13) {
      e.preventDefault();
    }
  }

  public handleClosePopUp() {
    this.props.history.push('/');
  }

  public render(): React.ReactNode {
    const formControlStyle = { padding: '10px 0px' };
    const rootEl = document.getElementById('root');

    return (
      <Grid container={true} justify="center">
        <Grid item={true} xs={10} sm={8} md={7} lg={6} xl={5}>
          <Card style={{ marginTop: 30, padding: 20 }}>
            <CardContent style={{ textAlign: 'center' }}>
              <form>
                <FormControl fullWidth={true} error={Boolean(this.state.passwordResetErrMsg)}>
                  <InputLabel htmlFor="email">メールアドレス</InputLabel>
                  <Input
                    id="email"
                    value={this.state.email}
                    onChange={this.handleChangeUsername}
                    onKeyPress={this.handleKeyPress}
                  />
                  {this.state.passwordResetErrMsg ? (
                    <FormHelperText>大学のメールアドレスを入力してください</FormHelperText>
                  ) : null}
                </FormControl>

                <FormControl fullWidth={true} style={formControlStyle} error={Boolean(this.state.passwordResetErrMsg)}>
                  {this.state.passwordResetErrMsg ? (
                    <FormHelperText>{this.state.passwordResetErrMsg}</FormHelperText>
                  ) : null}
                  <Button
                    style={{
                      marginTop: 16,
                      marginBottom: 8,
                      boxShadow: 'none',
                    }}
                    variant="contained"
                    color="primary"
                    onClick={this.handleClickPasswordReset}
                  >
                    パスワードリセット用メールを送信する
                  </Button>
                </FormControl>
              </form>
              {this.state.showPopUp && rootEl ? (
                <PopUp onClose={this.handleClosePopUp} rootEl={rootEl} msg={'メールを送信しました'} />
              ) : null}
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    );
  }
}

export default PasswordReset;
