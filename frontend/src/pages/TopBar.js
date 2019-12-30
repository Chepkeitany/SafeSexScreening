import React from "react";
import {
  AppBar,
  Box,
  Toolbar,
  Typography
} from '@material-ui/core';

export default () =>
<AppBar color="primary" position="static">
    <Toolbar variant="regular">
      <Box flexGrow={1}>
        <Typography color="inherit" variant="h6">
          Safe Sex Screen
        </Typography>
      </Box>
    </Toolbar>
</AppBar>

