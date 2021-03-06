import numpy as np
import itertools


def fill_hist_adc_samples(data_stream, output_filename, histogram):

    for i, event in enumerate(data_stream):

        for telescope_id in event.r0.tels_with_data:

            data = event.r0.tel[telescope_id].adc_samples
            histogram.fill_with_batch(data)

        yield event

    histogram.save(output_filename)


def fill_hist_trigger_input_diff(event_stream, output_filename, histogram):

    for event in event_stream:

        for telescope_id in event.r0.tels_with_data:

            data = event.r0.tel[telescope_id].trigger_input_traces
            data = data - event.r0.tel[telescope_id].trigger_input_offline
            histogram.fill_with_batch(data)

        yield event

    histogram.save(output_filename)


def fill_hist_trigger_input(event_stream, output_filename, histogram):

    for event in event_stream:

        for telescope_id in event.r0.tels_with_data:

            data = event.r0.tel[telescope_id].trigger_input_traces
            histogram.fill_with_batch(data)

        yield event

    histogram.save(output_filename)


def fill_hist_cluster_7(event_stream, output_filename, histogram):

    for event in event_stream:

        for telescope_id in event.r0.tels_with_data:

            data = event.r0.tel[telescope_id].trigger_input_7
            histogram.fill_with_batch(data)

        yield event

    histogram.save(output_filename)


def fill_hist_cluster_19(event_stream, output_filename, histogram):

    for event in event_stream:

        for telescope_id in event.r0.tels_with_data:

            data = event.r0.tel[telescope_id].trigger_input_19
            histogram.fill_with_batch(data)

        yield event

    histogram.save(output_filename)


def fill_hist_trigger_time(event_stream, output_filename, histogram):

    t_old = 0

    for i, event in enumerate(event_stream):

        for telescope_id in event.r0.tels_with_data:

            t_new = event.r0.tel[telescope_id].local_camera_clock
            delta_t = t_new - t_old

            if i > 0:
                histogram.fill(delta_t)

            t_old = event.r0.tel[telescope_id].local_camera_clock

        yield event

    histogram.save(output_filename)


def save_dark(data_stream, output_filename, n_events=None):

    if n_events is None:

        iter_events = itertools.count()

    else:

        iter_events = range(n_events)

    for event, i in zip(data_stream, iter_events):

        for telescope_id in event.r0.tels_with_data:

            if i == 0:

                data = event.r0.tel[telescope_id].adc_samples
                baseline = np.zeros(data.shape[0])
                std = np.zeros(data.shape[0])

            data = event.r0.tel[telescope_id].adc_samples
            baseline += np.mean(data, axis=-1)
            std += np.std(data, axis=-1)

        yield event

    baseline /= i
    std /= i
    np.savez(output_filename, baseline=baseline, standard_deviation=std)


