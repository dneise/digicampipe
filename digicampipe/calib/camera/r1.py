import numpy as np
from digicampipe.utils import calib


def calibrate_to_r1(event_stream, dark_baseline):

    for event in event_stream:

        for telescope_id in event.r0.tels_with_data:

            # Get the R0 and R1 containers
            r0_camera = event.r0.tel[telescope_id]
            r1_camera = event.r1.tel[telescope_id]

            # Get the ADCs
            adc_samples = r0_camera.adc_samples
            baseline = r0_camera.baseline
            adc_samples = adc_samples - baseline[:, np.newaxis].astype(np.int16)
            r1_camera.adc_samples = adc_samples
            # Compute the gain drop and NSB

            if dark_baseline is None:
                # compute NSB and Gain drop from STD
                standard_deviation = r0_camera.standard_deviation
                r1_camera.gain_drop = calib.compute_gain_drop(standard_deviation, 'std')
                r1_camera.nsb = calib.compute_nsb_rate(standard_deviation, 'std')
            else:
                # compute NSB and Gain drop from baseline shift
                r0_camera.dark_baseline = dark_baseline['baseline']
                baseline_shift = baseline - r0_camera.dark_baseline
                r1_camera.gain_drop = calib.compute_gain_drop(baseline_shift, 'mean')
                r1_camera.nsb = calib.compute_nsb_rate(baseline_shift, 'mean')

        yield event

