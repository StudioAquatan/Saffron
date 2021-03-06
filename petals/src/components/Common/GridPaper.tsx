import Grid from '@material-ui/core/Grid';
import Paper from '@material-ui/core/Paper';
import * as React from 'react';

const GridPaper: React.FC<{ style?: React.CSSProperties }> = props => (
  <Grid container={true} justify="center">
    <Grid item={true} xs={12} sm={8} md={7} lg={6} xl={5}>
      <Paper style={{ marginTop: 20, padding: 30, boxShadow: 'none', ...props.style }}>{props.children}</Paper>
    </Grid>
  </Grid>
);

export default GridPaper;
