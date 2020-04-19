def load_params(net, async_net, params_path):
    net.load_parameters(params_path)
    async_net.load_parameters(params_path)


def save_params(net, best_mean_avg_prec, curr_mean_avg_prec, epoch, save_interval, prefix):
    curr_mean_avg_prec = float(curr_mean_avg_prec)
    if curr_mean_avg_prec > best_mean_avg_prec[0]:
        best_mean_avg_prec[0] = curr_mean_avg_prec
        net.save_params(f'{prefix}_{epoch}_{curr_mean_avg_prec}_best.params')
        with open(f'{prefix}_best_mean_avg_prec.log', 'a') as f:
            f.write(f'{epoch:04d}\t{curr_mean_avg_prec:.4f}\n')
    if not epoch % save_interval:
        net.save_params(f'{prefix}_{epoch:04d}_{curr_mean_avg_prec:.4f}.params')