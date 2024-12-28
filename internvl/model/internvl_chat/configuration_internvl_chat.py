# --------------------------------------------------------
# InternVL
# Copyright (c) 2023 OpenGVLab
# Licensed under The MIT License [see LICENSE for details]
# --------------------------------------------------------

import copy

from .configuration_internlm2 import InternLM2Config
from transformers import LlamaConfig, Qwen2Config
from transformers.configuration_utils import PretrainedConfig
from transformers.utils import logging

from .configuration_intern_vit import InternVisionConfig

logger = logging.get_logger(__name__)


class InternVLChatConfig(PretrainedConfig):
    model_type = 'internvl_chat'
    is_composition = True

    def __init__(
            self,
            vision_config=None,
            llm_config=None,
            use_backbone_lora=0,
            use_llm_lora=0,
            pad2square=False,
            select_layer=-1,
            force_image_size=None,
            downsample_ratio=0.5,
            template=None,
            dynamic_image_size=False,
            use_thumbnail=False,
            ps_version='v1',
            dynamic_max_patch=False,
            min_dynamic_patch=1,
            max_dynamic_patch=6,
            min_num_frame=4,
            max_num_frame=20,
            compress_seq=False,
            attn_type=None,
            group_list=None,
            chunk_num=1,
            interaction=True,
            rope_pos_id_version='default',
            rope_pos_id_stride=None,
            img_emb_down_sample_ratio=None,
            **kwargs):
        super().__init__(**kwargs)

        if vision_config is None:
            vision_config = {}
            logger.info('vision_config is None. Initializing the InternVisionConfig with default values.')

        if llm_config is None:
            llm_config = {}
            logger.info('llm_config is None. Initializing the LlamaConfig config with default values (`LlamaConfig`).')

        # import pdb; pdb.set_trace()
        self.vision_config = InternVisionConfig(**vision_config)
        if llm_config['architectures'][0] == 'LlamaForCausalLM':
            self.llm_config = LlamaConfig(**llm_config)
        elif llm_config['architectures'][0] == 'InternLM2ForCausalLM':
            self.llm_config = InternLM2Config(**llm_config)
        elif llm_config['architectures'][0] == 'Qwen2ForCausalLM':
            self.llm_config = Qwen2Config(**llm_config)
        else:
            raise ValueError('Unsupported architecture: {}'.format(llm_config['architectures'][0]))
        
        self.use_backbone_lora = use_backbone_lora
        self.use_llm_lora = use_llm_lora
        self.pad2square = pad2square
        self.select_layer = select_layer
        self.force_image_size = force_image_size
        self.downsample_ratio = downsample_ratio
        self.template = template
        self.dynamic_image_size = dynamic_image_size
        self.use_thumbnail = use_thumbnail
        self.ps_version = ps_version  # pixel shuffle version
        self.min_dynamic_patch = min_dynamic_patch
        self.max_dynamic_patch = max_dynamic_patch
        self.min_num_frame = min_num_frame
        self.max_num_frame = max_num_frame
        self.compress_seq = compress_seq
        self.attn_type=attn_type
        self.group_list = group_list
        self.chunk_num = chunk_num
        self.interaction = interaction
        self.rope_pos_id_version = rope_pos_id_version
        self.rope_pos_id_stride = rope_pos_id_stride
        self.img_emb_down_sample_ratio = img_emb_down_sample_ratio
        self.dynamic_max_patch = dynamic_max_patch
        logger.info(f'vision_select_layer: {self.select_layer}')
        logger.info(f'ps_version: {self.ps_version}')
        logger.info(f'dynamic_max_patch: {self.dynamic_max_patch}')
        logger.info(f'min_dynamic_patch: {self.min_dynamic_patch}')
        logger.info(f'max_dynamic_patch: {self.max_dynamic_patch}')
        logger.info(f'img_emb_down_sample_ratio: {self.img_emb_down_sample_ratio}')

    def to_dict(self):
        """
        Serializes this instance to a Python dictionary. Override the default [`~PretrainedConfig.to_dict`].

        Returns:
            `Dict[str, any]`: Dictionary of all the attributes that make up this configuration instance,
        """
        output = copy.deepcopy(self.__dict__)
        output['vision_config'] = self.vision_config.to_dict()
        output['llm_config'] = self.llm_config.to_dict()
        output['model_type'] = self.__class__.model_type
        output['use_backbone_lora'] = self.use_backbone_lora
        output['use_llm_lora'] = self.use_llm_lora
        output['pad2square'] = self.pad2square
        output['select_layer'] = self.select_layer
        output['force_image_size'] = self.force_image_size
        output['downsample_ratio'] = self.downsample_ratio
        output['template'] = self.template
        output['dynamic_image_size'] = self.dynamic_image_size
        output['use_thumbnail'] = self.use_thumbnail
        output['ps_version'] = self.ps_version
        output['min_dynamic_patch'] = self.min_dynamic_patch
        output['max_dynamic_patch'] = self.max_dynamic_patch
        output['dynamic_max_patch'] = self.dynamic_max_patch
        output['rope_pos_id_version'] = self.rope_pos_id_version
        output['rope_pos_id_stride'] = self.rope_pos_id_stride
        output['img_emb_down_sample_ratio'] = self.img_emb_down_sample_ratio
        output['min_num_frame'] = self.min_num_frame
        output['max_num_frame'] = self.max_num_frame

        return output
