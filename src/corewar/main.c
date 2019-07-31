/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: fdagbert <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2019/07/16 16:35:44 by fdagbert          #+#    #+#             */
/*   Updated: 2019/07/31 01:01:05 by fdagbert         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "corewar.h"

static int		ft_print_man(t_conf *conf)
{
	int		fd;

	fd = 0;
	if ((fd = open(D_MAN_PATH, O_RDONLY)) < 0)
		return (-22);
	ft_printf("##VISUOFF\n");
	if (conf->opt[5])
		ft_printf("{GRE}%~{OFF}\n", fd);
	else
		ft_printf("%~\n", fd);
	if (close(fd) < 0)
		return (-22);
	return (0);
}

static int		ft_init_fd(t_champ *champ, t_conf *conf)
{
	while (champ)
	{
		if ((champ->fd = open(champ->path, O_RDONLY)) < 0)
			return (-2);
		conf->players[champ->id] = champ;
		champ = champ->next;
	}
	if (!conf->nb_players)
		return (-5);
	if (conf->nb_players > MAX_PLAYERS)
		return (-6);
	return (0);
}

static int		ft_check_define(void)
{
	int		int_size;

	int_size = sizeof(int);
	if (REG_SIZE != int_size)
	{
		if (int_size == 4)
			return (-7);
		else if (int_size == 8)
			return (-8);
		else
			return (-9);
	}
	return (0);
}

static void		ft_print_winner(t_conf *conf)
{
	if (!conf->opt[0])
	{
		if (!(conf->last_live))
			ft_printf("Il n'y a pas de survivant...\n");
		else
			ft_printf("Le joueur %d(%s) a gagné !\n",
					conf->last_live, conf->players[conf->last_live]->name);
	}
}

int				main(int argc, char **argv)
{
	int					err;
	t_conf				conf;
	static const char	keys[D_OPT_MAX + 1] = {'d', 'v', 'a', 'x', 's', 'c',
		'n', 'h', 'b', 'e', 'm', 0};

	err = 0;
	ft_init_conf(0, &conf);
	ft_init_op(&conf);
	if ((err = ft_check_args(argc, argv, keys, &conf)) < 0)
		return (ft_end(err, &conf));
	if (conf.opt[7] || err == 1)
		return (ft_end(ft_print_man(&conf), &conf));
	if ((err = ft_init_fd(conf.first_player, &conf)) < 0)
		return (ft_end(err, &conf));
	if ((err = ft_check_define()) < 0)
		return (ft_end(err, &conf));
	if ((err = ft_champion_parser(conf.first_player, &conf)) < 0)
		return (ft_end(err, &conf));
	if ((err = ft_init_arena(0, conf.first_player, &conf)) < 0)
		return (ft_end(err, &conf));
	if ((err = ft_launch_arena(0, conf.first_process, &conf)) < 0)
		return (ft_end(err, &conf));
	if (!conf.opt[3])
		ft_print_winner(&conf);
	return (ft_end(err, &conf));
}