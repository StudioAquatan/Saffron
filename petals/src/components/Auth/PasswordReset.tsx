import Button from '@material-ui/core/Button';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogTitle from '@material-ui/core/DialogTitle';
import FormControl from '@material-ui/core/FormControl';
import FormHelperText from '@material-ui/core/FormHelperText';
import Grid from '@material-ui/core/Grid';
import TextField from '@material-ui/core/TextField';
import * as React from 'react';
import { RouteComponentProps } from 'react-router';
import { Field, InjectedFormProps, reduxForm, SubmissionError, WrappedFieldProps } from 'redux-form';

import * as passwordApi from '../../api/password';

interface FormParams {
  email: string;
}

interface PasswordResetProps extends RouteComponentProps<any>, InjectedFormProps {}

interface PasswordResetState {
  showDialog: boolean;
}

class PasswordReset extends React.Component<PasswordResetProps, PasswordResetState> {
  constructor(props: PasswordResetProps) {
    super(props);
    this.state = {
      showDialog: false,
    };
  }

  public handleCloseDialog = () => {
    this.props.history.push('/');
  };

  public renderTextField = (props: WrappedFieldProps & { label: string; type: string }) => (
    <FormControl fullWidth={true} error={Boolean(props.meta.error)} style={{ padding: '10px 0px' }}>
      <TextField label={props.label} margin="normal" type={props.type} {...props.input} />
      {props.meta.error ? <FormHelperText>{props.meta.error}</FormHelperText> : null}
    </FormControl>
  );

  public handleSubmit = (values: FormParams) => {
    const emailErrMsg = values.email ? '' : '未入力です';
    if (emailErrMsg) {
      throw new SubmissionError({ email: emailErrMsg, _error: '入力項目に誤りがあります' });
    }

    return passwordApi
      .reset(values.email)
      .then(() => {
        this.setState({ showDialog: true });
      })
      .catch((e: Error) => {
        // TODO: handling
        throw new SubmissionError({ _error: 'メール送信に失敗しました' });
      });
  };

  public render(): React.ReactNode {
    const formControlStyle = { padding: '10px 0px' };
    const { error, handleSubmit } = this.props;

    return (
      <Grid container={true} justify="center">
        <Grid item={true} xs={10} sm={8} md={7} lg={6} xl={5}>
          <Card style={{ marginTop: 30, padding: 20 }}>
            <CardContent style={{ textAlign: 'center' }}>
              <form onSubmit={handleSubmit(this.handleSubmit)}>
                <Field name="email" label="メールアドレス" type="text" component={this.renderTextField} />

                <FormControl fullWidth={true} style={formControlStyle} error={Boolean(error)}>
                  <Button
                    type="submit"
                    style={{
                      marginTop: 16,
                      marginBottom: 8,
                      boxShadow: 'none',
                    }}
                    variant="contained"
                    color="primary"
                  >
                    パスワードリセット用メールを送信する
                  </Button>
                  {error ? <FormHelperText>{error}</FormHelperText> : null}
                </FormControl>
              </form>
              <Dialog fullWidth={true} maxWidth="xs" open={this.state.showDialog} onClose={this.handleCloseDialog}>
                <DialogTitle>メールを送信しました</DialogTitle>
                <DialogActions>
                  <Button onClick={this.handleCloseDialog}>閉じる</Button>
                </DialogActions>
              </Dialog>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    );
  }
}

export default reduxForm({
  form: 'passwordResetForm',
})(PasswordReset);
