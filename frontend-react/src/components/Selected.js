import React from "react";

import { makeStyles } from "@material-ui/core/styles";
import Grid from "@material-ui/core/Grid";
import Paper from "@material-ui/core/Paper";
import Chip from "@material-ui/core/Chip";
import DoneIcon from "@material-ui/icons/Done";

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
    padding: theme.spacing(2),
  },
  chip: {
    margin: theme.spacing(0.5),
  },
}));

export default function Selected(props) {
  const classes = useStyles();

  const { chips, handleDelete } = props;
  return (
    <Grid container justify="center" className={classes.root} spacing={2}>
      <Grid xs={12} item>
        <Paper className={classes.root}>
          {chips.map((chip, id) => {
            const { type, label, color } = chip;
            return (
              <Chip
                key={id}
                className={classes.chip}
                label={label}
                color={color}
                onDelete={handleDelete(type, label)}
                // deleteIcon={<DoneIcon />}
              />
            );
          })}
        </Paper>
      </Grid>
    </Grid>
  );
}
