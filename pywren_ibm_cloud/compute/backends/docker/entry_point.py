import sys
import os
import uuid
import flask
import logging
import pkgutil
import multiprocessing

from pywren_ibm_cloud.version import __version__
from pywren_ibm_cloud.config import default_logging_config
from pywren_ibm_cloud.function import function_invoker

#default_logging_config(logging.INFO)

logging.basicConfig(filename='/tmp/pywren.logs/docker/proxy.log', level=logging.DEBUG)
logger = logging.getLogger('__main__')


proxy = flask.Flask(__name__)


@proxy.route('/', methods=['POST'])
def run():
    def error():
        response = flask.jsonify({'error': 'The action did not receive a dictionary as an argument.'})
        response.status_code = 404
        return complete(response)

    message = flask.request.get_json(force=True, silent=True)
    if message and not isinstance(message, dict):
        return error()

    act_id = str(uuid.uuid4()).replace('-', '')[:12]
    os.environ['__PW_ACTIVATION_ID'] = act_id

    if 'remote_invoker' in message:
        logger.info("PyWren v{} - Starting Docker invoker".format(__version__))
        message['config']['pywren']['compute_backend'] = 'localhost'
        if message['config']['pywren']['workers'] is None:
            total_cpus = multiprocessing.cpu_count()
            message['config']['pywren']['workers'] = total_cpus
            message['config']['localhost']['workers'] = total_cpus
        else:
            message['config']['localhost']['workers'] = message['config']['pywren']['workers']
        message['invokers'] = 0
        function_invoker(message)

    response = flask.jsonify({"activationId": act_id})
    response.status_code = 202

    return complete(response)


@proxy.route('/preinstalls', methods=['GET', 'POST'])
def preinstalls_task():
    logger.info("Extracting preinstalled Python modules...")

    runtime_meta = dict()
    mods = list(pkgutil.iter_modules())
    runtime_meta['preinstalls'] = [entry for entry in sorted([[mod, is_pkg] for _, mod, is_pkg in mods])]
    python_version = sys.version_info
    runtime_meta['python_ver'] = str(python_version[0])+"."+str(python_version[1])
    response = flask.jsonify(runtime_meta)
    response.status_code = 200
    logger.info("Done!")

    return complete(response)


def complete(response):
    # Add sentinel to stdout/stderr
    sys.stdout.write('%s\n' % 'XXX_THE_END_OF_AN_ACTIVATION_XXX')
    sys.stdout.flush()

    return response


def main():
    port = int(os.getenv('PORT', 8080))
    proxy.run(debug=True, host='0.0.0.0', port=port)


if __name__ == '__main__':
    main()
