import React from "react";

import { makeStyles } from "@material-ui/core/styles";
import Card from "@material-ui/core/Card";
import CardContent from "@material-ui/core/CardContent";
import Typography from "@material-ui/core/Typography";
import Chip from "@material-ui/core/Chip";
import DoneIcon from "@material-ui/icons/Done";

const useStyles = makeStyles((theme) => ({
  root: {
    minWidth: 275,
    display: "flex",
    justifyContent: "left",
    flexWrap: "wrap",
    "& > *": {
      margin: theme.spacing(0.5),
    },
  },
  chip: {
    margin: theme.spacing(0.5),
  },
}));

export default function MovieCard(props) {
  const classes = useStyles();

  const { chips, handleClick, handleDelete } = props;
  const { id, title } = props.movie;
  return (
    <Card className={classes.root}>
      <CardContent>
        <Typography color="textSecondary" gutterBottom>
          {id}
        </Typography>
        <Typography variant="h5" component="h2">
          {title}
        </Typography>
        {chips.map((chip, id) => {
          const { type, label, color, variant } = chip;
          return (
            <Chip
              key={id}
              className={classes.chip}
              label={label}
              color={color}
              variant={variant}
              onClick={handleClick(type, label)}
              onDelete={handleDelete(type, label)}
            />
          );
        })}
      </CardContent>
    </Card>
  );
}
